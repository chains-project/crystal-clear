import React, { useState, useCallback, useEffect, useRef } from "react";
// import { useSearchParams } from "react-router";
import Header from "../../components/layout/Header";
import Sidebar from "../../components/layout/Sidebar";
import GraphLayout from "../../components/graph/GraphLayout";
import type { GraphData, Node } from "../../components/graph/GraphLayout";
import { useLocalAlert } from "@/components/ui/local-alert";
import { fetchGraphData } from "@/utils/graphFetcher";
import '../../App.css';
import { getApiAvailability, getDeploymentInfo } from "@/utils/queries";
import type { DeploymentInfo as DeploymentInfoJSON } from "@/utils/queries";

export default function ContractGraph() {
    const [jsonData, setJsonData] = useState<GraphData | null>(null);
    const [deploymentInfo, setDeploymentInfo] = useState<DeploymentInfoJSON | null>(null);
    const [activeTab, setActiveTab] = useState<string>("Risk Score");
    const [inputAddress, setInputAddress] = useState<string>("");
    const [loading, setLoading] = useState<boolean>(false);
    const [fromBlock, setFromBlock] = useState<string>("");
    const [toBlock, setToBlock] = useState<string>("");
    const [selectedNode, setSelectedNode] = useState<Node | null>(null);
    const [highlightAddress, setHighlightAddress] = useState<string | null>(null);
    const { showLocalAlert } = useLocalAlert();
    // const [searchParams] = useSearchParams();
    const [apiAvailability, setApiAvailability] = useState<boolean | undefined>(undefined);

    const fetchData = useCallback(
        async (address: string, fromBlock: string, toBlock: string) => {
            if (!address) return;

            const isAvailable = await getApiAvailability();
            setApiAvailability(isAvailable);

            setLoading(true);

            console.log("address in graph", address);
            console.log("fromBlock in graph", fromBlock);
            console.log("toBlock in graph", toBlock);

            try {
                const data = await fetchGraphData(
                    address,
                    fromBlock,
                    toBlock,
                    (message) => showLocalAlert(message, 5000)
                );

                if (data) {
                    setJsonData(data);
                    // Automatically switch to Risk tab after data is loaded
                    setActiveTab("Risk Details");
                }
            } catch (error) {
                console.error("Error fetching graph data:", error);
                showLocalAlert("Failed to fetch graph data. Please try again later.", 5000);
                // Reset or clear state if needed
                setJsonData(null);
            } finally {
                setLoading(false);
            }
        },
        [fromBlock, toBlock, showLocalAlert]
    );

    // Read address from URL parameters when component mounts
    useEffect(() => {
        const searchParams = new URLSearchParams(location.search);
        const addressParam = searchParams.get('address');
        const fromBlockParam = searchParams.get('from_block');
        const toBlockParam = searchParams.get('to_block');

        console.log("addressParam in graph", addressParam);
        console.log("fromBlockParam in graph", fromBlockParam);
        console.log("toBlockParam in graph", toBlockParam);
        console.log("apiAvailability in graph", apiAvailability);

        if (addressParam) {
            setInputAddress(addressParam);
            // Only fetch data once when component mounts
            fetchData(
                addressParam,
                fromBlockParam || "",
                toBlockParam || ""
            );
        }
    }, []);

    const alertRef = useRef(showLocalAlert);
    alertRef.current = showLocalAlert;

    useEffect(() => {
        if (!inputAddress || apiAvailability === undefined) return;

        const fetch = async () => {
            try {
                const info = await getDeploymentInfo(inputAddress, apiAvailability, alertRef.current);
                setDeploymentInfo(prev => {
                    if (JSON.stringify(prev) === JSON.stringify(info)) return prev;
                    return info;
                });
            } catch (e) {
                alertRef.current("Failed to fetch deployment info", 5000);
            }
        };
        fetch();
    }, [inputAddress, apiAvailability]);


    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (inputAddress) {
            fetchData(inputAddress, fromBlock, toBlock);
        }
    };

    // Handle node click from the graph
    const handleNodeClick = useCallback((node: Node) => {
        setSelectedNode(node);
        setActiveTab("Dependency");
    }, []);

    // useEffect(() => {
    //     // Check if the page is being reloaded
    //     const navigationEntries = performance.getEntriesByType("navigation") as PerformanceNavigationTiming[];
    //     if (navigationEntries[0]?.type === "reload") {
    //         // Redirect to the graph page
    //         window.location.href = `${window.location.origin}/graph`; // Adjust the path as needed
    //     }
    // }, []);

    // deploymentInfo


    return (
        <div
            style={{
                height: "100vh",
                width: "100vw",
                display: "flex",
                flexDirection: "column",
                overflow: "hidden",
            }}
        >
            <Header
                inputAddress={inputAddress}
                setInputAddress={setInputAddress}
                fromBlock={fromBlock}
                setFromBlock={setFromBlock}
                toBlock={toBlock}
                setToBlock={setToBlock}
                handleSubmit={handleSubmit}
            />

            <div
                style={{
                    display: "flex",
                    height: "calc(100vh - 60px)",
                    width: "100%",
                    overflow: "hidden",
                }}
            >
                {/* Set explicit width to 61.8% for the graph container */}
                <div style={{ width: "61.8%", height: "100%", overflow: "hidden" }}>
                    <GraphLayout
                        jsonData={jsonData}
                        highlightAddress={highlightAddress}
                        inputAddress={inputAddress}
                        onNodeClick={handleNodeClick}
                    />
                </div>

                {/* Set explicit width to 38.2% for the sidebar */}
                <div style={{ width: "38.2%", height: "100%", overflow: "auto" }}>
                    <Sidebar
                        activeTab={activeTab}
                        setActiveTab={setActiveTab}
                        loading={loading}
                        jsonData={jsonData}
                        deploymentInfo={deploymentInfo}
                        inputAddress={inputAddress}
                        setHighlightAddress={setHighlightAddress}
                        highlightAddress={highlightAddress}
                        fromBlock={fromBlock ? parseInt(fromBlock) : null}
                        toBlock={toBlock ? parseInt(toBlock) : null}
                        selectedNode={selectedNode}
                        setSelectedNode={setSelectedNode}
                    />
                </div>
            </div>
        </div>
    );
}