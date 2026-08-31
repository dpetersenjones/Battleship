import React from "react"

export default function RedXSvg() {

    return (
        <svg width="40" height="40" viewBox="0 0 40 40" style={{zIndex:2}}>
            <line x1="10" y1="10" x2="30" y2="30" stroke="red" strokeWidth="4" />
            <line x1="30" y1="10" x2="10" y2="30" stroke="red" strokeWidth="4" />
        </svg>
    )
}