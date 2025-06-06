from typing import Any, Dict, Optional, List

from loguru import logger
from scsc.supply_chain import SupplyChain

from sqlmodel import Session

from core.config import settings
from core.exceptions import InputValidationError, InternalServerError
from core.metadata import get_labels
from core.database import get_session
import crud.label
from services.info_service import get_verification_data, get_proxy_data, get_permissions, get_scorecard_data
from services.contract_service import ContractService

def analyze_contract_dependencies(
    session: Session,
    address: str,
    from_block: Optional[str] = None,
    to_block: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Analyze contract dependencies.

    Args:
        address: Contract address to analyze
        from_block: Start block (optional)
        to_block: End block (optional)

    Returns:
        Dict containing the analysis results

    Raises:
        InputValidationError: If the input is invalid
        InternalServerError: If the analysis fails
    """
    try:
        # Perform analysis
        logger.info(f"Analyzing contract {address}")

        _validate_block_range(from_block, to_block)
        sc = SupplyChain(settings.eth_node_url, address)
        network = sc.get_network(from_block, to_block)
        network["nodes"] = _process_node_labels(session, network)
        network["edges"] = assess_edge_risk(network.get("edges", []))
        logger.info(f"Analysis completed for {address}")
        return network

    except ValueError as e:
        logger.error(f"Analyze contract dependencies: {e}")
        raise InputValidationError(str(e)) from e
    except Exception as e:
        logger.error(f"Internal server error: {e}")
        raise InternalServerError(f"Failed to analyze contract: {str(e)}") from e

def _validate_block_range(from_block: Optional[str], to_block: Optional[str]) -> None:
    """Validate the block range if provided."""
    if to_block is not None and from_block is not None:
        try:
            if int(to_block) - int(from_block) > settings.MAX_BLOCK_RANGE:
                raise ValueError(
                    f"Block range exceeds maximum limit of {settings.MAX_BLOCK_RANGE} blocks."
                )
        except ValueError:
            raise ValueError("Block numbers must be valid integers")

def _process_node_labels(session: Session, network: Optional[Dict[str, Any]]) -> List[str]:
    if not network:
            raise Exception("No network data found")
    if "nodes" not in network:
        raise Exception("No nodes found in network data")
    if not isinstance(network["nodes"], list):
        raise Exception("Nodes data is not a list")
    nodes = network["nodes"]
    logger.info("Processing node labels.")
    logger.info("Fetching labels from database.")
    stored_labels = crud.label.get_labels(
        session, crud.label.AddressList(addresses=nodes)
    )
    logger.info(f"Stored labels: {stored_labels}")

    logger.info("Labels fetched from database.")
    missing_addresses = set(nodes) - set(stored_labels.keys())
    
    if not missing_addresses:
            return stored_labels

    # Fetch and store missing labels
    allium_labels = get_labels(list(missing_addresses), settings.allium_api_key)
    new_labels = {}

    for addr in missing_addresses:
        if allium_labels and addr.lower() in allium_labels:
            label = allium_labels[addr.lower()]
            new_labels[addr] = label
            logger.info(f"Label for {addr}: {label}")
            crud.label.create_label(
                session,
                crud.label.LabelCreate(address=addr, label=label)
            )
            logger.info(f"Label {label} for {addr} stored in database.")
        else:
            new_labels[addr] = addr
    return {**stored_labels, **new_labels}

def assess_edge_risk(edges: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    for edge in edges:
        if "DELEGATECALL" in edge["types"]:
            edge["risk"] = "High"
        else:
            edge["risk"] = "Low"
    return edges

async def calculate_contract_risk(address: str, session: Session) -> Dict[str, Any]:
    """
    Calculate risk score for a contract.

    Args:
        address: Contract address to analyze
        session: Database session for ContractService

    Returns:
        Dict containing risk score and factors

    Raises:
        ContractAnalysisError: If the analysis fails
        ExternalServiceError: If the external service is unavailable
    """
    logger.info(f"Analysing risk of contract {address}.")
    contract_service = ContractService(session)
    risk_factors = {}

    try:
        logger.info("Fetching verification data.")
        verification_data = get_verification_data(address)
        verification_dic = {"exact_match": 1, "match": 0.9, "": 0}
        verification_score = verification_dic.get(verification_data.get("match", ""), 0)
    except Exception as e:
        logger.error(f"Verification data fetch error: {e}")
        verification_score = 0
        risk_factors["verification"] = "Not verified"

    try:
        logger.info("Fetching proxy data.")
        data = get_proxy_data(address)
        proxy_type = data["type"]
        proxy_dic = {"Not a proxy": 1, "Forward proxy": 0.8, "Upgradeable proxy": 0}
        print(f"Proxy type: {proxy_type}")
        proxy_score = proxy_dic.get(proxy_type, 0)
        if proxy_type == "Upgradeable proxy":
            risk_factors["mutability"] = "Upgradeable proxy"
    except Exception as e:
        logger.error(f"Proxy data fetch error: {e}")
        proxy_score = 0
    try:
        logger.info("Fetching permissions data.")
        permissions_data = get_permissions(address)
        permissions_score = 1 if len(permissions_data) == 0 else 0
    except Exception as e:
        logger.error(f"Permissions data fetch error: {e}")
        permissions_score = 0

    try:
        logger.info("Fetching scorecard data.")
        repo_data = await contract_service.get_contract_repository(address)
        url = repo_data["repository"].url
        url_elms = url.split("/")
        org, repo = url_elms[-2], url_elms[-1]
        scorecard_data = get_scorecard_data(org, repo)
        scorecard_score = scorecard_data["raw"]["score"]
        scorecard_score = scorecard_score / 10
    except Exception as e:
        logger.error(f"Scorecard data fetch error: {e}")
        scorecard_score = 0
        risk_factors["repository"] = "Not available"

    try:
        logger.info("Fetching contract audits.")
        audits_data = await contract_service.get_contract_audits(address)
        max_audits = 6
        audits_score = len(audits_data["audits"]) / max_audits
    except Exception as e:
        logger.error(f"Contract audits fetch error: {e}")
        audits_score = 0
    if audits_score == 0:
        risk_factors["audits"] = "No audits found"

    logger.info(f"Verification score: {verification_score}, Proxy score: {proxy_score}, Permissions score: {permissions_score}, Scorecard score: {scorecard_score}, Audits score: {audits_score}")

    score = 0.1 * verification_score + 0.05 * proxy_score + 0.05 * permissions_score + 0.3 * scorecard_score + 0.5 * audits_score
    risk_score = round((1-score) * 100)
    return {"risk_score": risk_score, "risk_factors": risk_factors}
