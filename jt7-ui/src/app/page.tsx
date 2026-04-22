"use client";

import { useState } from "react";

type JobStatus =
  | "Cold"
  | "Applied"
  | "Recruiter Contacted"
  | "Screening"
  | "Interviewing"
  | "Offer"
  | "Rejected";

type Job = {
  id: string;
  company: string;
  role: string;
  status: JobStatus;
  source: string;
  lastActivity: string;
  reason?: string;
};

type ActivityItem = {
  id: string;
  type: string;
  source: string;
  label: string;
  time: string;
};

const navItems = ["Dashboard", "Jobs", "Recruiters", "Activity", "Command"];
const footerItems = ["Settings", "System Status"];

const jobs: Job[] = [
  {
    id: "job_cigar_place_creative_designer_email_marketing_specialist",
    company: "Cigar Place",
    role: "Creative Designer & Email Marketing Specialist",
    status: "Cold",
    source: "Indeed",
    lastActivity: "Found Apr 3",
    reason: "No response in 2 days",
  },
  {
    id: "job_match_group_lead_product_designer",
    company: "Match Group",
    role: "Lead Product Designer",
    status: "Applied",
    source: "LinkedIn",
    lastActivity: "Application confirmed",
    reason: "Awaiting reply",
  },
  {
    id: "job_ezcater_senior_product_designer",
    company: "ezCater",
    role: "Senior Product Designer, Delivery & Fulfillment",
    status: "Applied",
    source: "Greenhouse",
    lastActivity: "Application confirmed",
  },
  {
    id: "job_deloitte_lead_ux_designer",
    company: "Deloitte",
    role: "Lead UX Designer, Agentic AI Platform",
    status: "Interviewing",
    source: "Indeed",
    lastActivity: "Interview tomorrow",
    reason: "Interview within 48h",
  },
  {
    id: "job_realpage_product_designer",
    company: "RealPage",
    role: "Product Designer I - UX",
    status: "Recruiter Contacted",
    source: "iCIMS",
    lastActivity: "Recruiter replied",
    reason: "Recruiter replied — no action logged",
  },
];

const activity: ActivityItem[] = [
  {
    id: "a1",
    type: "Application confirmed",
    source: "Gmail",
    label: "Match Group / Lead Product Designer",
    time: "23m ago",
  },
  {
    id: "a2",
    type: "Recruiter outreach",
    source: "Gmail",
    label: "RealPage / Product Designer I - UX",
    time: "1h ago",
  },
  {
    id: "a3",
    type: "Interview scheduled",
    source: "Gmail",
    label: "Deloitte / Lead UX Designer",
    time: "3h ago",
  },
  {
    id: "a4",
    type: "Lead added",
    source: "Job Search",
    label: "Cigar Place / Creative Designer & Email Marketing Specialist",
    time: "2d ago",
  },
];

const statusOrder: JobStatus[] = [
  "Cold",
  "Applied",
  "Recruiter Contacted",
  "Screening",
  "Interviewing",
  "Offer",
  "Rejected",
];

const statusClass: Record<JobStatus, string> = {
  Cold: "status-cold",
  Applied: "status-applied",
  "Recruiter Contacted": "status-recruiter",
  Screening: "status-screening",
  Interviewing: "status-interviewing",
  Offer: "status-offer",
  Rejected: "status-rejected",
};

function countByStatus(status: JobStatus) {
  return jobs.filter((job) => job.status === status).length;
}

export default function Home() {
  const needsAttention = jobs.filter((job) => job.reason);
  const [selectedJobId, setSelectedJobId] = useState(jobs[0]?.id ?? "");
  const selectedJob = jobs.find((job) => job.id === selectedJobId) ?? jobs[0];

  return (
    <div className="flex min-h-screen bg-background text-foreground">
      <aside className="hidden w-60 shrink-0 border-r border-border bg-surface lg:flex lg:flex-col">
        <div className="border-b border-border px-5 py-4">
          <div className="text-xs uppercase tracking-[0.2em] text-muted">JT7</div>
          <div className="mt-1 text-lg font-semibold">Job Command Center</div>
        </div>

        <nav className="flex-1 px-3 py-4">
          <ul className="space-y-1">
            {navItems.map((item) => {
              const active = item === "Dashboard";
              return (
                <li key={item}>
                  <button
                    className={`flex w-full items-center justify-between rounded-xl px-3 py-2 text-left text-sm transition ${
                      active
                        ? "border border-border bg-surface-elevated text-foreground"
                        : "text-muted hover:bg-surface-elevated hover:text-foreground"
                    }`}
                  >
                    <span>{item}</span>
                    {item === "Jobs" && needsAttention.length > 0 ? (
                      <span className="rounded-full border border-border px-2 py-0.5 text-xs text-foreground">
                        {needsAttention.length}
                      </span>
                    ) : null}
                  </button>
                </li>
              );
            })}
          </ul>
        </nav>

        <div className="border-t border-border px-3 py-4">
          <ul className="space-y-1">
            {footerItems.map((item) => (
              <li key={item}>
                <button className="flex w-full items-center rounded-xl px-3 py-2 text-left text-sm text-muted transition hover:bg-surface-elevated hover:text-foreground">
                  {item}
                </button>
              </li>
            ))}
          </ul>
        </div>
      </aside>

      <div className="flex min-w-0 flex-1 flex-col">
        <header className="sticky top-0 z-10 flex h-14 items-center justify-between gap-4 border-b border-border bg-background/95 px-4 backdrop-blur lg:px-6">
          <div className="flex min-w-0 flex-1 items-center gap-3">
            <div className="rounded-lg border border-border bg-surface px-3 py-2 text-sm text-muted w-full max-w-xl">
              Search or type a command
            </div>
          </div>
          <div className="flex items-center gap-3">
            <div className="rounded-full border border-border bg-surface px-3 py-1.5 text-xs text-foreground">
              Connected
            </div>
          </div>
        </header>

        <main className="flex min-h-0 flex-1 overflow-hidden">
          <div className="min-w-0 flex-1 overflow-y-auto px-4 py-6 lg:px-6">
            <div className="mx-auto flex max-w-7xl flex-col gap-8">
              <section className="space-y-4">
                <div>
                  <h1 className="text-2xl font-semibold tracking-tight">Dashboard</h1>
                  <p className="mt-1 text-sm text-muted">Current pipeline state</p>
                </div>

                <div className="rounded-2xl border border-border bg-surface p-4">
                  <div className="mb-4 flex items-center justify-between">
                    <div>
                      <h2 className="text-base font-semibold">Needs Attention</h2>
                      <p className="mt-1 text-sm text-muted">What needs action now</p>
                    </div>
                    <span className="rounded-full border border-border px-2.5 py-1 text-xs text-foreground">
                      {needsAttention.length} items
                    </span>
                  </div>
                  <div className="space-y-3">
                    {needsAttention.map((job) => (
                      <button
                        key={job.id}
                        onClick={() => setSelectedJobId(job.id)}
                        className="flex w-full items-start justify-between rounded-xl border border-border bg-surface-elevated px-4 py-3 text-left transition hover:border-[#2b2b31]"
                      >
                        <div>
                          <div className="text-sm font-medium">{job.company}</div>
                          <div className="mt-1 text-sm text-muted">{job.role}</div>
                        </div>
                        <div className="text-sm text-right text-foreground">{job.reason}</div>
                      </button>
                    ))}
                  </div>
                </div>

                <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-6">
                  {statusOrder.map((status) => (
                    <div key={status} className="rounded-2xl border border-border bg-surface p-4">
                      <div className={`text-sm font-medium ${statusClass[status]}`}>{status}</div>
                      <div className="mt-3 text-2xl font-semibold">{countByStatus(status)}</div>
                    </div>
                  ))}
                </div>
              </section>

              <section className="grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
                <div className="rounded-2xl border border-border bg-surface p-4">
                  <div className="mb-4">
                    <h2 className="text-base font-semibold">Jobs</h2>
                    <p className="mt-1 text-sm text-muted">Scan the current pipeline</p>
                  </div>

                  <div className="overflow-hidden rounded-xl border border-border">
                    <table className="w-full border-collapse text-left text-sm">
                      <thead className="bg-surface-elevated text-muted">
                        <tr>
                          <th className="px-4 py-3 font-medium">Company</th>
                          <th className="px-4 py-3 font-medium">Role</th>
                          <th className="px-4 py-3 font-medium">Status</th>
                          <th className="px-4 py-3 font-medium">Source</th>
                        </tr>
                      </thead>
                      <tbody>
                        {jobs.map((job) => {
                          const selected = job.id === selectedJobId;
                          return (
                            <tr
                              key={job.id}
                              onClick={() => setSelectedJobId(job.id)}
                              className={`cursor-pointer border-t border-border transition ${
                                selected ? "bg-surface-elevated" : "hover:bg-surface-elevated/70"
                              }`}
                            >
                              <td className="px-4 py-3 font-medium">{job.company}</td>
                              <td className="px-4 py-3 text-muted">{job.role}</td>
                              <td className={`px-4 py-3 ${statusClass[job.status]}`}>{job.status}</td>
                              <td className="px-4 py-3 text-muted">{job.source}</td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                </div>

                <div className="rounded-2xl border border-border bg-surface p-4">
                  <div className="mb-4">
                    <h2 className="text-base font-semibold">Recent Activity</h2>
                    <p className="mt-1 text-sm text-muted">Simplified Gmail-derived signals</p>
                  </div>
                  <div className="space-y-3">
                    {activity.map((item) => (
                      <div key={item.id} className="rounded-xl border border-border bg-surface-elevated px-4 py-3">
                        <div className="flex items-start justify-between gap-3">
                          <div>
                            <div className="text-sm font-medium">{item.type}</div>
                            <div className="mt-1 text-sm text-muted">{item.label}</div>
                          </div>
                          <div className="text-xs text-muted">{item.time}</div>
                        </div>
                        <div className="mt-2 text-xs uppercase tracking-[0.18em] text-muted">{item.source}</div>
                      </div>
                    ))}
                  </div>
                </div>
              </section>
            </div>
          </div>

          <aside className="hidden w-[360px] shrink-0 border-l border-border bg-surface xl:block">
            <div className="border-b border-border px-5 py-4">
              <div className="text-xs uppercase tracking-[0.18em] text-muted">Job Detail</div>
              <div className="mt-1 text-lg font-semibold">{selectedJob.company}</div>
              <div className="mt-1 text-sm text-muted">{selectedJob.role}</div>
            </div>

            <div className="space-y-6 px-5 py-5 text-sm">
              <section>
                <div className="mb-2 text-xs uppercase tracking-[0.18em] text-muted">Overview</div>
                <div className="space-y-3">
                  <div>
                    <div className="text-xs text-muted">Status</div>
                    <div className={`mt-1 font-medium ${statusClass[selectedJob.status]}`}>{selectedJob.status}</div>
                  </div>
                  <div>
                    <div className="text-xs text-muted">Source</div>
                    <div className="mt-1 font-medium">{selectedJob.source}</div>
                  </div>
                  <div>
                    <div className="text-xs text-muted">Last Activity</div>
                    <div className="mt-1 font-medium">{selectedJob.lastActivity}</div>
                  </div>
                </div>
              </section>

              <section>
                <div className="mb-2 text-xs uppercase tracking-[0.18em] text-muted">Primary Action</div>
                <button className="w-full rounded-xl border border-border bg-surface-elevated px-4 py-3 text-left font-medium transition hover:border-[#2b2b31]">
                  {selectedJob.status === "Cold"
                    ? "Mark as Applied"
                    : selectedJob.status === "Applied"
                      ? "Log Recruiter Contact"
                      : selectedJob.status === "Interviewing"
                        ? "Add Interview Notes"
                        : "Review Job"}
                </button>
              </section>
            </div>
          </aside>
        </main>
      </div>
    </div>
  );
}
