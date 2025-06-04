import React, { useState, useEffect } from "react";
import type { JsonData } from "../../types";
import InfoCard from "@/components/common/InfoCard";
import {
    getRiskAnalysis,
    getProxyInfo,
    getPermissionInfo,
    getVerificationInfo,
    getAuditInfo,
} from "../../utils/queries";


interface RiskDetailsProps {
    jsonData: JsonData | null;
}

interface RiskMetric {
    name: string;
    value: string;
    level: "high" | "medium" | "low";
    detail?: string;
}

export default function RiskDetails({ jsonData }: RiskDetailsProps) {
    const [riskMetrics, setRiskMetrics] = useState<RiskMetric[]>([]);
    const [loading, setLoading] = useState(false);

    const defaultMetrics: RiskMetric[] = [
        { name: "Immutability", value: "waiting", level: "medium" },
        { name: "Admin Privileges", value: "waiting", level: "medium" },
        { name: "Verification", value: "waiting", level: "medium" },
        { name: "Audit", value: "waiting", level: "medium" },
    ];

    useEffect(() => {
        if (jsonData?.address) {
            setRiskMetrics(defaultMetrics);
            showDetailedRiskData(jsonData.address);
        }
    }, [jsonData]);


    // const showDetailedRiskData = async (address: string) => {
    //     setLoading(true);

    //     try {
    //         const [proxyRes, permissionRes, verificationRes, auditRes] = await Promise.allSettled([
    //             getProxyInfo(address, true),
    //             getPermissionInfo(address, true),
    //             getVerificationInfo(address, true),
    //             getAuditInfo(address, true),
    //         ]);

    //         const updated: RiskMetric[] = [];

    //         // Proxy
    //         if (proxyRes.status === "fulfilled") {
    //             const proxy = proxyRes.value;
    //             const isProxy = proxy?.type?.toLowerCase() === "not a proxy";
    //             console.log(proxy?.type);
    //             updated.push({
    //                 name: "Immutability",
    //                 value: isProxy ? "immutable" : "proxy",
    //                 level: isProxy ? "low" : "high",
    //                 detail: "Proxy Type: " + proxy?.type + "\n" + "Proxy message: " + proxy?.message || "No additional message.",
    //             });
    //         } else {
    //             updated.push({
    //                 name: "Immutability",
    //                 value: "Cannot get",
    //                 level: "medium",
    //                 detail: "Failed to fetch proxy info.",
    //             });
    //         }

    //         // Permission
    //         if (permissionRes.status === "fulfilled") {
    //             const permission = permissionRes.value;
    //             const adminFuncs = Array.isArray(permission?.function) ? permission.function : [];

    //             updated.push({
    //                 name: "Admin Privileges",
    //                 value: adminFuncs.length > 0 ? "Found" : "None",
    //                 level: adminFuncs.length > 0 ? "high" : "low",
    //                 detail: adminFuncs.length > 0 ? "Admin functions: " + adminFuncs.join(", ") : "No admin function detected.",
    //             });
    //         } else {
    //             updated.push({
    //                 name: "Admin Privileges",
    //                 value: "Cannot get",
    //                 level: "medium",
    //                 detail: "Failed to fetch permission info.",
    //             });
    //         }
    //         // Verification
    //         if (verificationRes.status === "fulfilled") {
    //             const verification = verificationRes.value;
    //             const verified = verification?.verification?.toLowerCase().includes("verified");
    //             updated.push({
    //                 name: "Verification",
    //                 value: verified ? "verified" : "not verified",
    //                 level: verified ? "low" : "high",
    //                 detail: "Verification status: " + verification?.verification + "\n" + "Verified at " + verification?.verifiedAt || "No verification time found.",
    //             });
    //         } else {
    //             updated.push({
    //                 name: "Verification",
    //                 value: "Not Verified",
    //                 level: "medium",
    //                 detail: "This contract is not verified on the Sourcify.",
    //             });
    //         }
    //         // Audit
    //         if (auditRes.status === "fulfilled") {
    //             const audit = auditRes.value;
    //             const audits = audit?.audits || [];
    //             const protocol = audit?.contract?.protocol || "Unknown protocol";
    //             const version = audit?.contract?.version || "Unknown version";

    //             if (audits.length > 0) {
    //                 const auditDetails = audits.map((a, i) => {
    //                     return `🔹 Audit ${i + 1} by ${a.company}${a.url ? `\n ` : ""}`;
    //                 }).join("");

    //                 updated.push({
    //                     name: "Audit",
    //                     value: "Found",
    //                     level: "low",
    //                     detail: `Protocol: ${protocol}\nVersion: ${version}\n\n${auditDetails}`,
    //                 });
    //             } else {
    //                 updated.push({
    //                     name: "Audit",
    //                     value: "None",
    //                     level: "high",
    //                     detail: `Protocol: ${protocol}\nVersion: ${version}\n\nNo audit found.`,
    //                 });
    //             }
    //         } else {
    //             updated.push({
    //                 name: "Audit",
    //                 value: "Not found",
    //                 level: "medium",
    //                 detail: "We couldn't find any audit info.",
    //             })
    //         }

    //         setRiskMetrics(updated);
    //     } catch (error) {
    //         console.error("Unexpected error fetching risk data:", error);
    //     } finally {
    //         setLoading(false);
    //     }
    // };

    const showDetailedRiskData = async (address: string) => {
        setLoading(true);
        const updated: RiskMetric[] = [];

        try {
            // Proxy
            try {
                const proxy = await getProxyInfo(address, true);
                const isProxy = proxy?.type?.toLowerCase() === "not a proxy";
                updated.push({
                    name: "Immutability",
                    value: isProxy ? "immutable" : "proxy",
                    level: isProxy ? "low" : "high",
                    detail: `Proxy Type: ${proxy?.type || "N/A"}\nProxy message: ${proxy?.message || "No additional message."}`,
                });
            } catch {
                updated.push({
                    name: "Immutability",
                    value: "Cannot get",
                    level: "medium",
                    detail: "Failed to fetch proxy info.",
                });
            }

            // Permission
            try {
                const permission = await getPermissionInfo(address, true);
                const adminFuncs = Array.isArray(permission?.function) ? permission.function : [];
                updated.push({
                    name: "Admin Privileges",
                    value: adminFuncs.length > 0 ? "Found" : "None",
                    level: adminFuncs.length > 0 ? "high" : "low",
                    detail: adminFuncs.length > 0 ? `Admin functions: ${adminFuncs.join(", ")}` : "No admin function detected.",
                });
            } catch {
                updated.push({
                    name: "Admin Privileges",
                    value: "Cannot get",
                    level: "medium",
                    detail: "Failed to fetch permission info.",
                });
            }

            // Verification
            try {
                const verification = await getVerificationInfo(address, true);
                const verified = verification?.verification?.toLowerCase().includes("verified");
                updated.push({
                    name: "Verification",
                    value: verified ? "verified" : "not verified",
                    level: verified ? "low" : "high",
                    detail:
                        (verification?.verification ? `Verification status: ${verification.verification}\n` : "") +
                        (verification?.verifiedAt ? `Verified at: ${verification.verifiedAt}` : "No verification time found."),
                });
            } catch {
                updated.push({
                    name: "Verification",
                    value: "Not Verified",
                    level: "medium",
                    detail: "This contract is not verified on Sourcify.",
                });
            }

            // Audit
            try {
                const audit = await getAuditInfo(address, true);
                const audits = audit?.audits || [];
                const protocol = audit?.contract?.protocol || "Unknown protocol";
                const version = audit?.contract?.version || "Unknown version";

                if (audits.length > 0) {
                    const auditDetails = audits
                        .map((a, i) => `🔹 Audit ${i + 1} by ${a.company}${a.url ? `: ${a.url} \n` : ""}`)
                        .join("\n");

                    updated.push({
                        name: "Audit",
                        value: "Found",
                        level: "low",
                        detail: `Protocol: ${protocol}\nVersion: ${version}\n\n${auditDetails}`,
                    });
                } else {
                    updated.push({
                        name: "Audit",
                        value: "None",
                        level: "high",
                        detail: `Protocol: ${protocol}\nVersion: ${version}\n\nNo audit found.`,
                    });
                }
            } catch {
                updated.push({
                    name: "Audit",
                    value: "Not found",
                    level: "medium",
                    detail: "We couldn't find any audit info.",
                });
            }

            setRiskMetrics(updated);
        } catch (error) {
            console.error("Unexpected error fetching risk data:", error);
        } finally {
            setLoading(false);
        }
    };




    return (
        <div className="w-full min-h-full h-fit p-6 bg-white rounded-xl shadow-md border border-gray-200">

            {loading ? (
                <div className="mt-10 flex justify-center items-center">
                    <div className="mt-50 animate-pulse px-4 py-2 bg-red-100 border border-gray-200 rounded-md shadow-sm text-sm text-gray-500 italic" style={{ marginTop: "100px", padding: "10px" }}>
                        🔍 Fetching Risk Details...
                    </div>
                </div>
            ) : (
                <div style={{
                    display: "flex",
                    flexDirection: "column",
                    width: "100%",
                    padding: "10px",
                    gap: "10px",

                }}>
                    {riskMetrics.map((metric, index) => (
                        <InfoCard className="w-full"
                            key={index}
                            header={
                                <div className="w-full max-w-none" style={{
                                    borderBottom: "1px solid #497D74",
                                    paddingBottom: "4px",
                                    display: "flex",
                                    // justifyContent: "space-between",
                                    alignItems: "center",

                                }}>
                                    <span className="text-l font-medium text-gray-800" style={{ fontSize: "16px" }}>{metric.name}</span>
                                    <span style={{
                                        fontSize: "12px",
                                        textAlign: "right",
                                        marginLeft: "6px",
                                        padding: "4px",
                                    }}
                                        className={`text-xs font-semibold px-2 py-0.5 rounded
                  ${metric.level === "high"
                                                ? "bg-red-100 text-red-600"
                                                : metric.level === "medium"
                                                    ? "bg-orange-100 text-orange-600"
                                                    : "bg-green-100 text-green-600"}
                `}
                                    >
                                        {metric.value}
                                    </span>
                                </div>
                            }
                            content={
                                <div className="text-gray-600 whitespace-pre-line break-words whitespace-pre-wrap" style={{ fontSize: "14px" }}>
                                    {metric.detail || <span className="italic text-gray-400">No further details available.</span>}
                                </div>
                            }
                        />
                    ))}
                </div>
            )}
        </div>
    );
}
