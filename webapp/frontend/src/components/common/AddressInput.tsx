import React from "react";
import { Input } from "@/components/ui/input";
import { isAddress } from "ethers";

interface AddressInputProps {
    value: string;
    onChange: (value: string) => void;
    placeholder?: string;
    className?: string;
    style?: React.CSSProperties;
    showValidation?: boolean;
}

export function AddressInput({
    value,
    onChange,
    placeholder = "Enter contract address",
    className = "",
    style = {},
    showValidation = true,
}: AddressInputProps) {

    console.log("value", value);
    console.log("onChange", onChange);

    const isValid = value === "" || isAddress(value);

    console.log("isValid", isValid);

    return (
        <div
            style={{
                position: "relative",
                display: "flex",
                alignItems: "center",
                width: "100%",
                ...style,
            }}
            className={className}
        >
            <Input
                type="text"
                value={value}
                onChange={(e) => {
                    const val = e.target.value;
                    onChange(val);
                }}
                placeholder={placeholder}
                style={{
                    display: "flex",
                    color: "#2b2b2b",
                    height: "32px",
                    border: `1px solid ${!isValid && showValidation ? "#EF164F" : "#2b2b2b"
                        }`,
                    borderRightColor: "grey",
                    borderBottomColor: "grey",
                    borderRadius: "1px",
                    fontSize: "13px",
                    width: "100%",
                    paddingRight: "30px",
                    textAlign: "left",
                    // boxShadow: "inset -1px -1px #fff, inset 1px 1px grey, inset 2px 2px #fff, inset 2px 2px #fff"
                }}
            />

            {/* Clear button */}
            {value && (
                <div
                    style={{
                        position: "absolute",
                        right: "10px",
                        top: "50%",
                        transform: "translateY(-50%)",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        cursor: "pointer",
                        color: "#999",
                        zIndex: 10,
                        backgroundColor: "inherit",
                        borderRadius: "50%",
                        width: "16px",
                        height: "16px",
                    }}
                    onClick={() => onChange("")}
                >
                    <svg
                        width="14"
                        height="14"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    >
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                </div>
            )}

        </div>
    );
}