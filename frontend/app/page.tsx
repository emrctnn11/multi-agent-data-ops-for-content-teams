"use client";

import { useEffect, useState } from "react";
import axios from "axios";
import { createClient } from "@supabase/supabase-js";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
const supabase = createClient(supabaseUrl, supabaseKey);

interface WorkflowResponse {
  message: string;
  run_id: string;
  final_post: string;
  data: any;
}

interface BlogPost {
  id: string;
  created_at: string;
  prd_text: string;
  final_output: string;
  status: string;
}

export default function Home() {
  const [isMounted, setIsMounted] = useState(false);

  const [prdContent, setPrdContent] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  const [finalPost, setFinalPost] = useState<string>("");
  const [historyPosts, setHistoryPosts] = useState<BlogPost[]>([]);

  useEffect(() => {
    setIsMounted(true);
    fetchHistory();
    setupRealtimeSubscription();
  }, []);

  const fetchHistory = async () => {
    const { data, error } = await supabase
      .from("workflow_runs")
      .select("*")
      .eq("status", "completed")
      .order("created_at", { ascending: false });

    if (data) {
      setHistoryPosts(data);
    }
  };

  const setupRealtimeSubscription = () => {
    supabase
      .channel("public:workflow_runs")
      .on(
        "postgres_changes",
        {
          event: "*",
          schema: "public",
          table: "workflow_runs",
        },
        (payload) => {
          console.log("Change received!", payload);
          fetchHistory();
        }
      )
      .subscribe();
  };

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
      setFinalPost(response.data.final_post);
    } catch (error: any) {
      console.error("Error starting workflow:", error);
      setStatusMessage(`❌ An error occurred: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownloadPdf = async () => {
    if (!finalPost) {
      alert("No final post available to download.");
      return;
    }

    const html2pdf = (await import("html2pdf.js")).default;
    const element = document.getElementById("blog-content");

    const opt = {
      margin: [10, 10, 10, 10] as [number, number, number, number],
      filename: `blog-post-${new Date().toISOString().slice(0, 10)}.pdf`,
      image: { type: "jpeg" as const, quality: 0.98 },
      html2canvas: { scale: 2, useCORS: true },
      jsPDF: { unit: "mm", format: "a4", orientation: "portrait" as const },
    };

    html2pdf().set(opt).from(element!).save();
  };

  const loadFromHistory = (post: BlogPost) => {
    setFinalPost(post.final_output);
    setPrdContent(post.prd_text);
    setStatusMessage(`Loaded from history: ${post.id}`);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  if (!isMounted) {
    return null;
  }

  return (
    <main className="flex min-h-screen flex-col items-center p-12 bg-gray-50 text-black">
      {/* Header */}
      <div className="z-10 max-w-6xl w-full flex flex-col items-center justify-between font-mono text-sm lg:flex-row mb-8">
        <h1 className="text-4xl font-bold text-blue-600">
          AI Content Ops Agent
        </h1>
        <p className="text-gray-500 mt-2 lg:mt-0">
          Multi Agent Blog Generator Developed by Emre Cetin
        </p>
      </div>

      <div className="flex w-full max-w-6xl gap-8 flex-col lg:flex-row">
        <div className="flex-1 flex flex-col gap-6">
          <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200">
            <label className="block text-gray-700 text-lg font-bold mb-2">
              PRD / Content Requirements:
            </label>

            <textarea
              className="w-full h-32 p-4 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4 text-gray-800"
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
                className={`mt-4 p-3 rounded-lg text-sm ${
                  statusMessage.includes("✅")
                    ? "bg-green-100 text-green-800 border border-green-200"
                    : "bg-blue-100 text-blue-800 border border-blue-200"
                }`}
              >
                {statusMessage}
              </div>
            )}
          </div>

          {finalPost && (
            <div className="w-full">
              <div className="flex justify-between items-center mb-2">
                <h2 className="text-xl font-bold text-gray-800">
                  📝 Current View
                </h2>
                <button
                  onClick={handleDownloadPdf}
                  className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded flex items-center gap-2 shadow-md"
                >
                  📄 Download PDF
                </button>
              </div>
              <div
                id="blog-content"
                style={{
                  padding: "40px",
                  backgroundColor: "#ffffff",
                  color: "#333333",
                  border: "1px solid #e5e7eb",
                  borderRadius: "12px",
                  boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
                }}
              >
                <h2
                  style={{
                    fontSize: "24px",
                    fontWeight: "bold",
                    marginBottom: "20px",
                    borderBottom: "1px solid #e5e7eb",
                    paddingBottom: "10px",
                    color: "#111111",
                  }}
                >
                  ✨ Generated Blog Post
                </h2>

                <div
                  style={{
                    fontFamily: "sans-serif",
                    lineHeight: "1.6",
                    fontSize: "16px",
                    whiteSpace: "pre-wrap",
                  }}
                >
                  {finalPost}
                </div>

                <div
                  style={{
                    marginTop: "30px",
                    paddingTop: "15px",
                    borderTop: "1px solid #e5e7eb",
                    fontSize: "12px",
                    color: "#9ca3af",
                    textAlign: "center",
                  }}
                >
                  Generated by Multi Agent Blog Generator Developed by Emre
                  Cetin
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="w-full lg:w-1/3 flex flex-col gap-4">
          <h2 className="text-2xl font-bold text-gray-800 top-0 bg-gray-50 py-2 z-10">
            🕒 History ({historyPosts.length})
          </h2>

          <div className="flex flex-col gap-3 overflow-y-auto max-h-[80vh] pr-2">
            {historyPosts.length === 0 && (
              <p className="text-gray-400 italic">No completed posts yet.</p>
            )}

            {historyPosts.map((post) => (
              <div
                key={post.id}
                onClick={() => loadFromHistory(post)}
                className={`p-4 rounded-lg border cursor-pointer transition-all hover:shadow-md ${
                  finalPost === post.final_output
                    ? "bg-blue-50 border-blue-400 ring-2 ring-blue-200"
                    : "bg-white border-gray-200 hover:border-blue-300"
                }`}
              >
                <div className="flex justify-between items-start mb-2">
                  <span className="text-xs font-mono text-gray-400">
                    {new Date(post.created_at).toLocaleDateString()}
                  </span>
                  <span className="text-xs bg-green-100 text-green-800 px-2 py-0.5 rounded-full">
                    {post.status}
                  </span>
                </div>
                <p className="text-sm font-medium text-gray-800 line-clamp-2">
                  {post.prd_text}
                </p>
                <p className="text-xs text-blue-600 mt-2 font-semibold">
                  Click to View →
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}
