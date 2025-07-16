import logging
from typing import Any, Dict, List, Set

from hexbytes import HexBytes
from web3 import Web3


class TraceCollector:
    def __init__(self, url: str):
        """
        Initializes the TraceCollector with a URL and log level.
        """
        self.logger = logging.getLogger(self.__class__.__name__)

        self.w3 = Web3(Web3.HTTPProvider(url))
        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to the Ethereum node.")
        self.logger.info("Connected to the Ethereum node.")

        # Reference bytecode for "x0" - this should be the actual bytecode
        self.x0_bytecode = "x0"  # Replace with actual x0 bytecode

    def _validate_contract(self, address: str, block: str) -> bool:
        """
        Validates contract address and checks if it's different from x0
        """
        try:
            if address.startswith("0x000000000000000000000000000000000000000"):
                self.logger.error(f"Address is a precompile address: {address}")
                return False
            address = Web3.to_checksum_address(address)
            if not Web3.is_address(address):
                self.logger.error(f"Invalid contract address format: {address}")
                return False
            code = self.w3.eth.get_code(address, block_identifier=block)
            if len(code) == 0:
                self.logger.error(f"No code at address: {address}")
                return False

            if code.hex() == self.x0_bytecode:
                self.logger.info(f"Contract at {address} matches x0 contract")
                return False

            return True
        except Exception as e:
            self.logger.error(f"Error validating contract: {e}")
            return False

    def _filter_txs_from(
        self, from_block: str, to_block: str, contract_address: str
    ) -> Set[str]:
        """
        Filters transactions from a given block range and contract address.
        """
        self.logger.info(
            f"Filtering transactions from block {from_block} \
              to {to_block} for contract {contract_address}."
        )
        filter_params = {
            "fromBlock": from_block,
            "toBlock": to_block,
            "fromAddress": [contract_address],
        }
        try:
            res = self.w3.tracing.trace_filter(filter_params)
        except Exception as e:
            self.logger.error(f"Error filtering transactions: {e}")
            return set()

        if res is None:
            return set()
        tx_hashes = {
            (
                r["transactionHash"].to_0x_hex()
                if type(r["transactionHash"]) is HexBytes
                else r["transactionHash"]
            )
            for r in res
            if r["type"] == "call"
        }
        self.logger.info(f"Found {len(tx_hashes)} transactions.")
        return tx_hashes

    def _get_calls_from_tx(self, tx_hash: str) -> Dict[str, Any]:
        """
        Gets calls from a transaction hash.
        """
        self.logger.info(f"Tracing transaction {tx_hash}.")
        try:
            res = self.w3.geth.debug.trace_transaction(
                tx_hash, {"tracer": "callTracer"}
            )
        except Exception as e:
            self.logger.error(f"Error tracing transaction {tx_hash}: {e}")
            return {}
        return res

    def _extract_all_subcalls(
        self, call: Dict[str, Any], calls: List[Dict[str, str]], caller: str, depth: int = 0
    ) -> None:
        """
        Recursively extracts all subcalls from a call.
        """
        depth += 1
        key = (caller, call["to"])
        if key not in calls:
            calls[key] = {"source": caller, "target": call["to"], "types": {}, "depth": depth }
        if call["type"] not in calls[key]["types"]:
            calls[key]["types"][call["type"]] = 0
        calls[key]["types"][call["type"]] += 1
        calls[key]["depth"] = min(calls[key]["depth"], depth)

        for subcall in call.get("calls", []):
            self._extract_all_subcalls(subcall, calls, call["to"], depth)

    def _extract_calls(
        self,
        call: Dict[str, Any],
        contract_address: str,
        calls: List[Dict[str, str]],
    ) -> None:
        """
        Extracts calls from a call and its subcalls.
        """
        if call["to"].lower() == contract_address.lower():
            for subcall in call.get("calls", []):
                self._extract_all_subcalls(subcall, calls, call["to"], 0)
        else:
            for subcall in call.get("calls", []):
                self._extract_calls(subcall, contract_address, calls)

    def get_calls(
        self, tx_hashes: Set[str], contract_address: str
    ) -> List[Dict[str, str]]:
        """
        Gets calls for a given set of transaction hashes and contract address.
        """
        self.logger.info(f"Getting calls for contract {contract_address}.")
        calls = {}
        for h in tx_hashes:
            res = self._get_calls_from_tx(h)
            if res:
                self._extract_calls(res, contract_address, calls)
        self.logger.info(f"Extracted {len(calls)} calls.")
        return calls.values()

    def _filter_contract_calls(
        self, calls: List[Dict[str, str]], to_block
    ) -> List[Dict[str, str]]:
        """
        Filters calls to contract addresses.
        """
        return [
            c
            for c in calls
            if self._validate_contract(c["target"], to_block)
        ]

    def get_calls_from(
        self, from_block: str | int, to_block: str | int, contract_address: str
    ) -> List[Dict[str, str]]:
        """
        Gets calls from a given block range and contract address.
        """
        self.logger.info(
            f"Getting calls from block {from_block} \
            to {to_block} for contract {contract_address}."
        )
        from_block_hex = self.validate_and_convert_block(from_block)
        to_block_hex = self.validate_and_convert_block(to_block)

        if not self._validate_contract(contract_address, to_block_hex):
            raise ValueError("Invalid contract address or bytecode.")
        contract_address = Web3.to_checksum_address(contract_address)
        tx_hashes = self._filter_txs_from(
            from_block_hex, to_block_hex, contract_address
        )
        calls = self.get_calls(tx_hashes, contract_address)
        filtered_calls = self._filter_contract_calls(calls, to_block_hex)
        
        edges = filtered_calls
        nodes: Set[str] = set()
        for edge in edges:
            nodes.add(edge["source"])
            nodes.add(edge["target"])
        
        return {
            "contract_address": contract_address,
            "from_block": int(from_block_hex, 16),
            "to_block": int(to_block_hex, 16),
            "n_nodes": len(nodes),
            "nodes": list(nodes),
            "edges": edges,
            "n_matching_transactions": len(tx_hashes),
        }

    def get_network(
        self,
        contract_address: str,
        from_block: str | int | None,
        to_block: str | int | None,
        blocks: int = 10,
    ) -> dict:
        """
        Collects calls from the last 10 blocks and returns the call graph in JSON format.
        """
        if from_block is None and to_block is None:
            self.logger.info("Collecting calls from the last n blocks.")
            latest_block = self.w3.eth.block_number
            from_block = latest_block - blocks
            to_block = latest_block

        res =self.get_calls_from(from_block, to_block, contract_address)
        return res
    
    def validate_and_convert_block(self, block: str) -> str:
        """
        Validates if block number is decimal or hex and returns hex format.
        """
        if isinstance(block, int):
            return hex(block)

        if isinstance(block, str):
            if block.startswith("0x"):
                try:
                    int(block, 16)
                    return block
                except ValueError as e:
                    raise ValueError(f"Invalid hex block number: {block}") from e

            if block.isdigit():
                return hex(int(block))

        raise ValueError(
            f"Block number must be decimal or hexadecimal: {block}"
        ) from None