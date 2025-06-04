import React, { useState, useEffect, useCallback } from "react";
import { useLocation, useNavigate } from "react-router";
import GraphLayout from "../../components/graph/GraphLayout";
import { Button } from "@/components/ui/button";
import { getDefaultBlockRange } from "@/utils/defaultAnalyze";
import { popularContracts } from "@/utils/popularContracts";
import { AddressInput } from "@/components/common/AddressInput";
import { getLatestBlock, getApiAvailability } from "@/utils/queries";
import { validateBlockRange } from "@/utils/blockRange";
import { errorManager } from "@/utils/errorManager";
// load sample graph data from json file
import SAMPLE_GRAPH_DATA from "./home_graph_eg.json";
import { isAddress } from "ethers";

export default function HomePage() {
    const [inputAddress, setInputAddress] = useState<string>("");
    const [highlightAddress, setHighlightAddress] = useState<string | null>(null);
    const [apiAvailability, setApiAvailability] = useState<boolean | undefined>(undefined);
    const [loading, setLoading] = useState<boolean>(false);
    const isValid = inputAddress === "" || isAddress(inputAddress);

    const { errors, setError, clearError } = errorManager();
    const location = useLocation();
    const navigate = useNavigate();

    const latestBlockNumber = getLatestBlock(apiAvailability);



    // --- Effect: Load API health and query params ---
    useEffect(() => {
        (async () => {
            const available = await getApiAvailability();
            setApiAvailability(available);
            console.log("apiAvailability in homepage", available);
        })();

        const addressParam = new URLSearchParams(location.search).get("address");
        if (addressParam) setInputAddress(addressParam);
    }, [location]);


    // --- Handle form submission ---
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        clearError("form");

        if (loading) return;
        setLoading(true);

        try {
            if (!inputAddress.trim()) {
                return setError("form", "Please enter a contract address.");
            }

            if (!isAddress(inputAddress)) {
                return setError("form", "Invalid Ethereum address.");
            }

            if (!apiAvailability) {
                return setError("api", "API is not available. Please refresh the page.");
            }

            try {
                const resolvedLatestBlock = await latestBlockNumber;
                if (!resolvedLatestBlock) {
                    return setError("api", "Latest block number is not available.");
                }

                const { fromBlock, toBlock } = await getDefaultBlockRange(setError, resolvedLatestBlock, apiAvailability);
                const { valid, reason } = validateBlockRange(fromBlock, toBlock);
                if (!valid) {
                    return setError("form", reason || "Invalid block range.");
                }

                navigate(`/graph?address=${inputAddress}&from_block=${fromBlock}&to_block=${toBlock}`);

            } catch (error) {
                return setError("api", "Failed to fetch latest block number.");
            }



        }
        finally {
            setLoading(false);
        }
    };


    // --- Handle popular address selection ---
    const handleAddressSelect = (address: string) => {
        setInputAddress(prev => (prev === address ? "" : address));
    };

    // --- Handle node click in demo graph ---
    const handleNodeClick = useCallback(() => {
        setHighlightAddress(null);
    }, []);



    return (
        <div
            style={{
                width: "100vw",
                minHeight: "100vh",
                display: "flex",
                flexDirection: "column",
                backgroundColor: "#fff",
                // border: "1px solid red"
            }}
        >
            {/* Header Section */}
            <header style={{
                width: "100%",
                padding: "1rem",
                backgroundColor: "white",
                textAlign: "center",
                // borderBottom: "1px solid #ddd"
            }}>
                {/* TODO:Future navigation elements will go here */}
            </header>

            <div
                style={{
                    minHeight: "100vh",
                    display: "flex",
                    flex: "1",
                    width: "100%",
                    alignItems: "center",
                    // border: "1px solid orange",
                }}
            >
                {/* Left side: Interactive network graph visualization */}
                <div style={{
                    width: "50%",
                    height: "100%",
                    overflow: "hidden",
                    position: "relative",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    marginLeft: "2rem",
                    marginRight: "1rem",
                    padding: "1rem",
                    // borderRadius: "50%",
                    // border: "1px solid red"
                }}>
                    {/* Interactive sample graph */}
                    <GraphLayout
                        jsonData={SAMPLE_GRAPH_DATA as GraphData}
                        highlightAddress={highlightAddress}
                        inputAddress={"0xSampleMainContract"}
                        onNodeClick={handleNodeClick}
                        isHomepage={true}
                    />
                </div>

                {/* Right side: Name and search bar */}
                <div style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    width: "50%",
                    height: "80%",
                    overflow: "auto",
                    padding: "2rem",
                    marginRight: "2rem",
                    marginLeft: "1rem",
                    backgroundColor: "white"
                }}>
                    <div style={{
                        width: "100%",
                        backgroundColor: "white",
                        padding: "1.5rem",
                        borderRadius: "4px",
                        marginBottom: "1.5rem",

                    }}>
                        <h2 style={{ color: "#312750", marginBottom: "0.5rem", fontSize: "3rem", fontFamily: "Jersey 20, 'Funnel Sans'" }}>
                            Crystal Clear
                        </h2>
                        <p style={{ color: "#2b2b2b", marginBottom: "1rem", fontSize: "1.2rem" }}>
                            A Smart Contract Is Only as Secure as Its Weakest Dependency.
                        </p>

                        <div
                            style={{
                                display: "flex",
                                alignItems: "center",
                                paddingTop: "8px",
                                backgroundColor: "white",
                                gap: "8px",
                                justifyContent: "center",
                            }}
                        >
                            {/* Search form */}
                            <form onSubmit={handleSubmit} style={{
                                height: "100%",
                                marginTop: "1.5rem",
                                width: "100%",
                                display: "flex",
                                flexDirection: "column",
                                justifyContent: "left"
                            }}>
                                <div style={{ marginBottom: "1rem", width: "100%" }}>
                                    <div style={{
                                        display: "flex",
                                        width: "100%",
                                        gap: "0.5rem",
                                    }}>
                                        <AddressInput
                                            value={inputAddress}
                                            onChange={(value) => {
                                                setInputAddress(value);
                                                console.log("inputAddress in homepage", inputAddress);
                                            }}
                                            placeholder="Enter contract address (0x...)"
                                            style={{
                                                flex: 1,

                                            }}
                                        />
                                        <Button variant="outline"
                                            type="submit"
                                            style={{
                                                padding: "0 1.5rem",
                                                height: "auto",
                                                color: "#2b2b2b",
                                                borderRadius: "2px",
                                            }}
                                            disabled={loading}
                                        >
                                            {loading ? "Loading..." : "Analyze"}
                                        </Button>
                                    </div>
                                </div>

                                {/* Popular Protocols Section */}
                                <div
                                    style={{
                                        display: "flex",
                                        flexDirection: "column",
                                        // alignItems: "left",
                                        // justifyContent: "left",
                                        paddingTop: "8px",
                                        paddingBottom: "8px",
                                        backgroundColor: "white",
                                        gap: "8px",
                                    }}
                                >
                                    <span
                                        style={{
                                            fontSize: "14px",
                                            color: "#666",
                                            whiteSpace: "nowrap",
                                            justifyContent: "left",

                                        }}
                                    >
                                        Try protocols:
                                    </span>
                                    <div style={{
                                        display: "grid",
                                        gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))", // Adjusts columns based on available space
                                        gap: "8px",
                                        overflow: "hidden",
                                        paddingBottom: "4px",
                                        justifyContent: "center",
                                        // border: "1px solid red"
                                    }}>

                                        {popularContracts.map((contract, index) => (
                                            <Button
                                                key={index}
                                                variant="link"
                                                type="button"
                                                onClick={() =>
                                                    handleAddressSelect(contract.address)
                                                }
                                                style={{
                                                    padding: "6px 6px",
                                                    height: "1.75rem",
                                                    fontSize: "12px",
                                                    whiteSpace: "nowrap",
                                                    overflow: "hidden",
                                                    textOverflow: "ellipsis",
                                                    borderRadius: "2px",
                                                    backgroundColor: "#f0f0f0",
                                                    color: "#2b2b2b",
                                                    // border: "1px solid #ccc",
                                                    // transition: "background-color 0.3s",
                                                }}
                                                onMouseEnter={(e) => e.currentTarget.style.backgroundColor = "#e0e0e0"}
                                                onMouseLeave={(e) => e.currentTarget.style.backgroundColor = "#f0f0f0"}
                                            >
                                                {contract.name}
                                            </Button>
                                        ))}
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>



        </div>
    );
}

