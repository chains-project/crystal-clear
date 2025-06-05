// components/common/InfoCard.tsx
import React from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

interface InfoCardProps {
    title?: string;
    header?: React.ReactNode;
    content: React.ReactNode;
    className?: string;
}

export default function InfoCard({ title, header, content, className = "" }: InfoCardProps) {
    return (
        <Card
            className={`shadow-lg z-50 w-fit ${className}`}
            style={{
                backgroundColor: "#fcfcf7",
                backdropFilter: "blur(8px)",
                border: "1px solid #497D74",
                borderRadius: "6px",
                padding: "6px",
                textAlign: "left",
                fontSize: "12px",
                boxShadow: "0 0 2px 0 rgba(0, 0, 0, 0.1)",
            }}
        >
            {(title || header) && (
                <CardHeader className="pb-2 space-y-1 m-0">
                    {title && <CardTitle className="text-xs m-0 font-semibold text-gray-700">{title}</CardTitle>}
                    {header}
                </CardHeader>
            )}

            <CardContent className="p-4 pt-2 space-y-2 text-[12px] text-muted-foreground text-left">
                {content}
            </CardContent>
        </Card>
    );
}
