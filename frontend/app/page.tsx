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
    if (!prdContent.trim()) {
      alert("Please enter PRD content.");
      return;
    }

    setIsLoading(true);
    setStatusMessage("Starting workflow...");

    try {
      const response = await axios.post<WorkflowResponse>(
        "http://127.0.0.1:8000/start-workflow",
        {
          prd_content: prdContent,
        }
      );

      setStatusMessage(
        `✅ Progress is done! Progress ID: ${response.data.run_id}`
      );
    } catch (error: any) {
      console.error("Error starting workflow:", error);
      setStatusMessage(`❌ An error occurred: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gray-50 text-black">
      {/* header */}

      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex mb-8">
        <h1 className="text-4xl font-bold text-blue-600">
          AI Content Ops Agent
        </h1>

        <p className="text-gray-500">Multu Agent Blog Generator</p>
      </div>

      {/* PRD input area */}
      <div className="w-full max-w-2xl bg-white p-8 rounded-xl shadow-lg border border-gray-200">
        <label className="block text-gray-700 text-lg font-bold mb-2">
          PRD / Content Requirements:
        </label>

        <textarea
          className="w-full h-40 p-4 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4 text-gray-800"
          placeholder="Example: Write a comprehensive blog post about the benefits of AI in modern healthcare..."
          value={prdContent}
          onChange={(e) => setPrdContent(e.target.value)}
        />

        <button
          onClick={handleStartWorkflow}
          disabled={isLoading}
          className={`w-full font-bold py-3 px-4 rounded-lg transition-all ${
            isLoading
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-blue-600 hover:bg-blue-700 text-white"
          }`}
        >
          {isLoading ? "Working... ⏳" : "Start Workflow 🚀"}
        </button>

        {statusMessage && (
          <div
            className={`mt-6 p-4 rounded-lg ${
              statusMessage.includes("✅")
                ? "bg-green-100 text-green-800 border border-green-200"
                : "bg-blue-100 text-blue-800 border border-blue-200"
            }`}
          >
            <p className="font-medium">{statusMessage}</p>
          </div>
        )}
      </div>
    </main>
  );
}
