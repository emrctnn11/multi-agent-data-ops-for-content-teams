"use client";

import { useState } from "react";
import axios from "axios";

// define type for response data

interface WorkflowResponse {
  message: string;
  run_id: string;
  data: any; 
}

export default function Home() {
  // define variables as States

  const [prdContent, setPrdContent] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  const handleStartWorkflow = async () => {
    if(!prdContent.trim()) {
      alert("Please enter PRD content.");
      return;
    }

    setIsLoading(true);
    setStatusMessage("Starting workflow...");
  
    try{
      const response = await axios.post<WorkflowResponse>(
        "http://127.0.0.1:8000/start-workflow",
        {
          prd_content: prdContent,
        }
      );

      setStatusMessage(`✅ Progress is done! Progress ID: ${response.data.run_id}`);
    } catch (error: any) {
      console.error("Error starting workflow:", error);
      setStatusMessage(`❌ An error occurred: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  }
}