"use client";
import { createContext, useContext, useEffect, useState } from "react";

export type JobType = "qa" | "search" | "code" | "docs";

export type Job = {
  id: string;
  issueId: string;
  issueTitle: string;
  workspaceId: string;  // add this
  status: "running" | "done" | "error";
  type: JobType;
  question: string;
  answer: string;
  searchResults?: { file_path: string; content: string; lines: string; language: string }[];
  codeResult?: unknown;
  docsResult?: string;
  sources?: { file: string; lines: string }[];
};

type JobsContextType = {
  jobs: Job[];
  startJob: (issueId: string, issueTitle: string, question: string, type: JobType, workspaceId: string) => string;
  appendChunk: (id: string, chunk: string) => void;
  finishJob: (id: string, status: "running" | "done" | "error", result?: Partial<Job>) => void;
  getJob: (issueId: string, type: JobType, workspaceId: string) => Job | undefined;
};

const JobsContext = createContext<JobsContextType>(null!);

export function JobsProvider({ children }: { children: React.ReactNode }) {
  const [jobs, setJobs] = useState<Job[]>(() => {
    try {
      const saved = localStorage.getItem("otto-jobs");
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  useEffect(() => {
    try {
      const persisted = jobs.map(j =>
        j.status === "running" ? { ...j, status: "error" as const } : j
      );
      localStorage.setItem("otto-jobs", JSON.stringify(persisted));
    } catch { /* storage full or unavailable */ }
  }, [jobs]);

  const startJob = (issueId: string, issueTitle: string, question: string, type: JobType, workspaceId: string) => {
    const id = `${issueId}-${type}-${Date.now()}`;
    setJobs(prev => [
      ...prev,
      { id, issueId, issueTitle, workspaceId, status: "running", type, question, answer: "" }
    ]);
    return id;
  };

  const appendChunk = (id: string, chunk: string) => {
    setJobs(prev => prev.map(j => j.id === id ? { ...j, answer: j.answer + chunk } : j));
  };

  const finishJob = (id: string, status: "running" | "done" | "error", result?: Partial<Job>) => {
    setJobs(prev => prev.map(j =>
      j.id === id ? { ...j, status, ...result } : j
    ));
  };

  const getJob = (issueId: string, type: JobType, workspaceId: string) =>
    jobs.filter(j => j.issueId === issueId && j.type === type && j.workspaceId === workspaceId).at(-1);

  return (
    <JobsContext.Provider value={{ jobs, startJob, appendChunk, finishJob, getJob }}>
      {children}
    </JobsContext.Provider>
  );
}

export const useJobs = () => useContext(JobsContext);