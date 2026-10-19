# Day 1 - State Diagram & Flow

## End-to-End Flow
1. Capture/Select -> User selects file in mobile app
2. Local Staging -> File saved in temp + validation (size/type)
3. Upload -> Chunk upload starts
4. Server Response -> UPLOADED
5. Processing Events -> Thumbnail / Transcode etc
6. Final Result -> PROCESSED

## State Diagram (Mermaid)
```mermaid
stateDiagram-v2
    [*] --> SELECTED
    SELECTED --> STAGING: validate & stage
    SELECTED --> CANCELLED: user cancel
    STAGING --> UPLOADING: start
    STAGING --> FAILED: validation fail
    STAGING --> CANCELLED
    UPLOADING --> UPLOADED: 200 OK
    UPLOADING --> FAILED: timeout/network
    UPLOADING --> CANCELLED
    UPLOADED --> PROCESSING: server event
    PROCESSING --> PROCESSED: success
    PROCESSING --> FAILED: processing error
    FAILED --> UPLOADING: retry (bounded)
    FAILED --> STAGING: restart