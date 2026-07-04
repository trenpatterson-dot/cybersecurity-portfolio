# GitHub Cleanup Recommendations

These recommendations are written from a recruiter-readiness perspective. They are not deletion instructions. Do not archive, delete, or make a repo private until Tren reviews the repo in GitHub.

## Evidence Limitations

Local repo evidence was available for:

- `trenpatterson-dot/cybersecurity-portfolio`
- `trenpatterson-dot/blue-team-command-center`
- `trenpatterson-dot/cybersecurity-site-portfolio`

The GitHub CLI was not installed in this environment, and the GitHub connector did not expose the public portfolio repo list. Treat repo-size and visibility checks as manual GitHub follow-up items.

## Repos That Should Stay Public

| Repo | Recommendation | Recruiter Reason |
| --- | --- | --- |
| `cybersecurity-portfolio` | Keep public after README and safety review | Main broad portfolio index for SOC, IAM, threat hunting, and blue-team labs. |
| `blue-team-command-center` | Keep public | Strongest Microsoft SOC analyst case series and best recruiter path for Sentinel, Defender XDR, Entra ID, IAM/RBAC, Purview, and Identity Protection work. |
| `cybersecurity-site-portfolio` | Keep public | Supports the live recruiter-facing portfolio site at https://cybersecurity-site-portfolio.vercel.app/. |
| `trenpatterson-dot` | Keep public if created as profile README repo | Gives recruiters a clean landing page before they inspect individual repos. |

## Repos That Should Maybe Be Archived

| Repo | Recommendation | Recruiter Reason |
| --- | --- | --- |
| `cybersecurity-portfolio-site` | Review in GitHub; archive if it is empty, duplicate, or replaced by `cybersecurity-site-portfolio` | Empty or duplicate public repos create confusion and make the portfolio look unfinished. The brief flagged this repo as public with size 0, but that still needs manual confirmation in GitHub. |
| Old duplicate lab repos | Archive only after confirming the stronger version exists in `cybersecurity-portfolio` or `blue-team-command-center` | Recruiters should see one polished version of each project, not several partial copies. |

## Repos That Should Maybe Be Made Private

| Repo Type | Recommendation | Recruiter Reason |
| --- | --- | --- |
| Draft job-search, affiliate, local-agent, or supervisor tooling repos | Make private if they contain personal workflow notes, generated drafts, job-search artifacts, or non-portfolio automation | These can distract from the SOC analyst story and may expose private process details. |
| Repos containing raw evidence, screenshots, exports, or logs that have not passed safety review | Make private until reviewed | Public evidence must be sanitized and approved before it supports the portfolio. |
| Repos with schoolwork, assignments, or non-cyber drafts | Make private unless they directly support the cybersecurity portfolio and are approved for public sharing | Keeps the GitHub profile focused on target roles. |

## Repos That Need README Improvements

| Repo | README Need | Recruiter Reason |
| --- | --- | --- |
| `cybersecurity-portfolio` | Add a recruiter start path and point to Blue Team Command Center as the current Microsoft SOC case series | Recruiters need a fast path through the strongest evidence. |
| `blue-team-command-center` | Remove stale duplicate table entries and keep legacy work lower than current SOC-018 to SOC-024 series | The newest Microsoft SOC story should be the first signal. |
| `cybersecurity-site-portfolio` | Expand the README with purpose, stack, setup, recruiter value, sections, and public-safe note | The live site repo should look as professional as the site it supports. |
| `trenpatterson-dot` | Add profile README content if the repo exists | The GitHub profile should immediately explain target roles, strengths, and featured work. |

## Manual GitHub Settings To Review

- Pin `blue-team-command-center`, `cybersecurity-portfolio`, and `cybersecurity-site-portfolio` on the GitHub profile.
- Set profile display name to `Tren Patterson` if it is not already set.
- Add concise repo descriptions for the three main public repos.
- Confirm whether `cybersecurity-portfolio-site` is empty or duplicate before archiving.
- Confirm public/private state for draft, job-search, affiliate, and local-agent repos.