import InfoCard from "@/components/common/InfoCard";

interface NodeHoverCardProps {
    nodeId: string;
    nodeInfo: any;
}

export default function NodeHoverCard({ nodeId, nodeInfo }: NodeHoverCardProps) {
    const content = (
        <>
            <div className="flex gap-1">
                <span className="text-muted-foreground">Address:</span>
                <span className="break-all">{nodeId}</span>
            </div>

            {nodeInfo === null || Object.keys(nodeInfo).length === 0 ? (
                <p className="text-muted-foreground">Loading node data...</p>
            ) : nodeInfo.error ? (
                <div className="space-y-1 text-sm text-foreground">
                    <div>
                        <span className="font-medium text-muted-foreground">Balance: </span>
                        <span className="italic text-gray-400">500</span>
                    </div>
                    <div>
                        <span className="font-medium text-muted-foreground">Company: </span>
                        <span className="italic text-gray-400">CCinc</span>
                    </div>
                </div>
            ) : (
                <div className="space-y-1 text-sm text-foreground">
                    <div>
                        <span className="font-medium text-muted-foreground">Balance:</span>
                        <span>{nodeInfo.balance}</span>
                    </div>
                    <div>
                        <span className="font-medium text-muted-foreground">Company:</span>
                        <span>{nodeInfo.company}</span>
                    </div>
                </div>
            )}
        </>
    );

    return <InfoCard content={content} className="min-w-[200px] max-w-sm text-[10px] absolute bottom-5 left-5" />;
}
