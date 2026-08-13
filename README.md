<div align="center">

# Kidney Exchange Matching System

### Turning incompatible donor pairs into compatible transplant chains, using real graph theory and optimization

[![Python](https://img.shields.io/badge/python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/frontend-React-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev/)
[![OR-Tools](https://img.shields.io/badge/solver-Google%20OR--Tools-4285F4?style=flat-square&logo=google&logoColor=white)](https://developers.google.com/optimization)
[![NetworkX](https://img.shields.io/badge/graph%20engine-NetworkX-2E8B57?style=flat-square)](https://networkx.org/)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](./LICENSE)
[![Status](https://img.shields.io/badge/status-active%20development-orange?style=flat-square)]()
[![Hackathon](https://img.shields.io/badge/built%20for-NSUT%20Hackathon-purple?style=flat-square)]()

<br/>

**[Live demo](#) &nbsp;•&nbsp; [Problem statement](#the-problem) &nbsp;•&nbsp; [How it works](#how-it-works) &nbsp;•&nbsp; [Architecture](#architecture) &nbsp;•&nbsp; [Benchmarks](#benchmarks) &nbsp;•&nbsp; [Getting started](#getting-started) &nbsp;•&nbsp; [References](#references)**

</div>

<br/>

<div align="center">
  <img src="docs/assets/demo.gif" alt="Live demo of a three way kidney exchange cycle being detected and highlighted on the compatibility graph" width="720"/>
  <p><i>Placeholder</i></p>
</div>

<br/>

## Table of contents

- [The problem](#the-problem)
- [The idea, in one paragraph](#the-idea-in-one-paragraph)
- [How it works](#how-it-works)
- [Architecture](#architecture)
- [What makes this different from a typical hackathon project](#what-makes-this-different-from-a-typical-hackathon-project)
- [Current build status](#current-build-status)
- [Features](#features)
- [Tech stack](#tech-stack)
- [Project structure](#project-structure)
- [Getting started](#getting-started)
- [API reference](#api-reference)
- [Benchmarks](#benchmarks)
- [Screenshots](#screenshots)
- [Roadmap](#roadmap)
- [Contributing and git workflow](#contributing-and-git-workflow)
- [References](#references)
- [Team](#team)
- [License](#license)

<br/>

## The problem

As of mid 2026, roughly 90,000 to 100,000 people are on the kidney transplant waiting list in the United States alone, and the median wait for a first kidney transplant is measured in years, not months. On average, around a dozen people die every single day while still waiting for a match. This isn't a niche medical inconvenience, it's one of the largest and most persistent supply gaps in modern healthcare.

A huge part of the problem isn't a lack of willing donors. Many patients already have a family member or friend who wants to donate a kidney to them directly. The problem is biology: the donor's blood type or tissue markers don't match the patient's, so a direct transplant would be rejected by the patient's immune system. This is called an incompatible pair, and it happens far more often than most people expect.

Here's the insight that real kidney exchange programs are built on: even though donor A cannot give to patient A, donor A's kidney might be a perfect match for patient B, whose own donor, donor B, might in turn be a perfect match for patient A. Neither pair could complete a transplant alone, but together they can, through a coordinated swap. Extend this logic across a pool of hundreds of incompatible pairs, and you get three way swaps, four way swaps, and long donor chains kicked off by a single altruistic, non directed donor. Programs like the National Kidney Registry have used this exact mechanism to complete chains involving as many as 70 participants, and roughly three quarters of all transplants facilitated through major kidney paired donation networks now happen through chains rather than simple pairwise swaps.

This project builds that matching engine from scratch: the graph model, the cycle search, and the optimization layer that decides which swaps actually go ahead.

<br/>

## The idea, in one paragraph

Model every incompatible patient-donor pair as a node in a directed graph. Draw an edge from pair A to pair B whenever A's donor is medically compatible with B's patient. Once the graph is built, the matching problem becomes a graph problem: find a set of node disjoint cycles (bounded to length 2 or 3, since longer cycles require every surgery to happen simultaneously across every hospital involved) plus open chains starting from altruistic donors, such that the total number of matched patients is maximized. This is exactly the problem real national kidney exchange clearinghouses solve every single day, and it happens to sit in a genuinely interesting complexity class: pairwise matching is solvable in polynomial time, but anything involving 3 way cycles or larger becomes NP-hard, which is why real programs lean on integer programming rather than brute force.

<br/>

## How it works

1. **Generate or ingest patient-donor pairs.** Each pair carries a patient blood type, a donor blood type, and a simulated crossmatch compatibility score. For the demo, a synthetic generator produces realistic pools using population level blood type distributions instead of uniform random data, so the numbers you see in the dashboard actually mean something.

2. **Build the compatibility graph.** Every pair becomes a node. A directed edge is added from pair A to pair B when A's donor could safely donate to B's patient. This is handled with NetworkX so the graph itself is inspectable, exportable, and easy to visualize.

3. **Enumerate candidate cycles.** A bounded search finds every cycle of length 2 and length 3 in the graph. The length cap of 3 isn't arbitrary, it mirrors the real world constraint that every surgery in a cycle has to happen on the same day, in every hospital involved, since no donor can be asked to wait and risk the other side of the swap falling through.

4. **Solve for the optimal set of disjoint cycles.** This is where the actual optimization happens. Each candidate cycle becomes a binary decision variable, and an integer program, solved with Google OR-Tools' CP-SAT solver, picks the combination of non overlapping cycles that maximizes total patients matched. A greedy baseline algorithm runs alongside it, picking the highest value cycles first, so the project can show, with real numbers, exactly how much better the optimal solution is and at what computational cost.

5. **Visualize the result.** The frontend renders the pool as a ring, every pair is a point on a circle, since a matched swap is literally a closed loop. Matched cycles glow and animate, so a viewer watches a swap light up in real time instead of reading a results table.

<br/>

## Architecture

```mermaid
flowchart TB
    subgraph DATA[Data layer]
        GEN[Synthetic pair generator]
        RULES[Compatibility rules engine]
        GEN --> RULES
    end

    subgraph CORE[Algorithm core, pure Python]
        GRAPH[Directed compatibility graph]
        CYCLES[Bounded cycle enumerator, length 2 to 3]
        CHAINS[Chain builder for altruistic donors]
        ILP[ILP optimal matcher, OR-Tools]
        GREEDY[Greedy baseline matcher]
        GRAPH --> CYCLES
        GRAPH --> CHAINS
        CYCLES --> ILP
        CYCLES --> GREEDY
        CHAINS --> ILP
    end

    subgraph SERVICE[Service layer]
        API[FastAPI backend: match, benchmark, dataset endpoints]
    end

    subgraph UI[Frontend]
        VIZ[React graph visualization with live cycle highlighting]
        DASH[Impact dashboard]
    end

    RULES --> GRAPH
    ILP --> API
    GREEDY --> API
    API --> VIZ
    API --> DASH
```

The separation between the algorithm core and the API layer is intentional: the matching engine is a standalone Python library with its own tests, runnable and benchmarkable with zero web framework involved. This is what lets you demonstrate, in a terminal, that the actual computer science works, before a single line of frontend code runs.

<br/>

## What makes this different from a typical hackathon project

Most social impact hackathon projects in this space end up being a form that calls an AI API and generates a summary. This project deliberately avoids that pattern. There is no language model anywhere in the matching pipeline. Every match that gets suggested is the output of a deterministic, verifiable algorithm that can be explained on a whiteboard, and that mirrors a decision making process actually used in production by real transplant networks.

The parts worth highlighting to judges:

- A real NP-hard-adjacent optimization problem, solved with an actual ILP formulation, not a heuristic dressed up as one.
- A quantified comparison between the optimal solver and a greedy baseline, so the value of "doing it properly" is shown with numbers and a chart, not asserted.
- A visual, animated demonstration of the exact mechanism, a cycle of pairs lighting up on a live graph, that makes the abstract idea instantly understandable to a non technical judge.
- Grounding in the actual academic literature and actual production systems, both cited below, rather than a reinvented wheel.

<br/>

## Current build status

The full pipeline works end to end now, terminal, API, and frontend all verified against each other, not just in isolation.

| Stage | What it proves | Status |
|---|---|---|
| Synthetic pairs generated | Realistic patient-donor pool exists | Verified |
| Compatibility graph built | Pairs correctly connected by ABO rules | Verified |
| Candidate cycles found | Valid 2 way and 3 way swaps identified | Verified |
| Optimal set selected | Best possible combination of swaps chosen, via ILP | Verified |
| Greedy baseline compared | Quantifies the gap against the optimal solver | Verified |
| Benchmark suite run | Real match rate and runtime numbers produced | Verified, see Benchmarks below |
| API live | All five endpoints tested through the interactive `/docs` page | Verified |
| Frontend built | Full graph view, dashboard, control panel, and benchmark chart, built against the real API | Build verified, a final look-at-it-in-a-real-browser pass is still worth doing before demo day |

The project is functionally complete for a working prototype. What's left is polish: the demo gif and screenshots, and the stretch goals below.

<br/>

## Features

| Feature | Description | Status |
|---|---|---|
| Synthetic dataset generator | Produces realistic patient-donor pools using population level blood type distributions | Done |
| Compatibility graph builder | Converts a pair pool into a directed graph using NetworkX | Done |
| Bounded cycle enumeration | Finds every valid 2 way and 3 way exchange cycle | Done |
| ILP optimal matcher | Maximizes total matched patients using Google OR-Tools | Done |
| Greedy baseline matcher | Fast approximate matcher, benchmarked against the optimal solver | Done |
| Benchmark suite | Compares match rate and runtime of optimal vs greedy across pool sizes | Done |
| REST API | FastAPI endpoints for running matches, generating data, and fetching benchmarks | Done |
| Interactive graph visualization | Renders the compatibility pool as a ring and animates matched cycles | Done |
| Impact dashboard | Shows patients matched with versus without exchange, side by side | Done |
| Altruistic donor chains | Supports open ended chains started by non directed donors | Planned, stretch goal |

<br/>

## Tech stack

<table>
<tr>
<td valign="top" width="33%">

**Algorithm core**
- Python 3.11+
- NetworkX
- Google OR-Tools (CP-SAT solver)
- pytest for correctness tests

</td>
<td valign="top" width="33%">

**Backend service**
- FastAPI
- Uvicorn
- Pydantic for request and response models

</td>
<td valign="top" width="33%">

**Frontend**
- React + Vite
- A custom SVG ring layout for the graph view, matched cycles animate on it directly
- Recharts for the benchmark chart

</td>
</tr>
</table>

<br/>

## Project structure

```
kidney-exchange-matching/
├── backend/
│   ├── algorithm_core/
│   │   ├── models.py            # Patient, Donor, IncompatiblePair, done
│   │   ├── generator.py         # synthetic dataset generator, done
│   │   ├── compatibility.py     # blood type and crossmatch rules, done
│   │   ├── graph_builder.py     # builds the directed compatibility graph, done
│   │   ├── cycle_finder.py      # bounded length cycle enumeration, done
│   │   ├── optimal_matcher.py   # ILP formulation and solver, done
│   │   ├── greedy_matcher.py    # greedy baseline, done
│   │   ├── chain_finder.py      # altruistic donor chain construction, not started
│   │   ├── demo.py              # runnable end to end terminal demo, done
│   │   └── tests/
│   ├── api/
│   │   ├── main.py               # FastAPI app entrypoint, done
│   │   ├── pipeline.py           # shared generate-graph-cycles helper, done
│   │   ├── routes/                # dataset, graph, match, benchmark, done
│   │   └── schemas/               # request/response shapes, done
│   ├── benchmarks/
│   │   └── run_benchmarks.py     # done, see Benchmarks below
│   ├── requirements.txt
│   └── pytest.ini
├── frontend/
│   ├── index.html
│   ├── vite.config.js
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── api/
│   │   │   └── client.js          # every backend call lives here, done
│   │   └── components/
│   │       ├── GraphView.jsx      # the ring layout, done
│   │       ├── ImpactDashboard.jsx
│   │       ├── ControlPanel.jsx   # pool size, seed, optimal/greedy toggle
│   │       └── BenchmarkChart.jsx
│   └── package.json
├── data/
│   └── sample_pairs.csv
├── docs/
│   ├── assets/                   # screenshots, gifs, diagrams, still placeholders
│   └── architecture.md
├── .gitignore
├── LICENSE
└── README.md
```

<br/>

## Getting started

These steps assume you have Python 3.11 or newer and Node.js 18 or newer installed.

**1. Clone the repository**

```bash
git clone https://github.com/your-username/kidney-exchange-matching.git
cd kidney-exchange-matching
```

**2. Set up the backend**

```bash
cd backend
python -m venv venv
source venv/bin/activate        # on Windows, use venv\Scripts\activate
pip install -r requirements.txt
```

This creates an isolated Python environment so the project's dependencies don't clash with anything else installed on your machine, then installs everything the algorithm core and API need.

**3. Run the algorithm core on its own, no server required**

```bash
python -m algorithm_core.demo
```

This runs the full pipeline end to end on a small synthetic dataset, dataset generation, graph construction, cycle detection, and both matchers, and prints the results straight to the terminal. Useful for proving the algorithm works before touching the web layer at all.

**4. Start the API server**

```bash
uvicorn api.main:app --reload
```

The API is available at `http://localhost:8000`, with interactive documentation at `http://localhost:8000/docs`, where every endpoint can be tested directly in the browser.

**5. Set up and run the frontend**

```bash
cd ../frontend
npm install
npm run dev
```

Open the printed local URL in your browser. Set a pool size, pick optimal or greedy, and run a match to see the ring light up.

<br/>

## API reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/dataset/generate` | Generates a synthetic pool of incompatible patient-donor pairs |
| `POST` | `/graph/build` | Builds the compatibility graph from a given pair pool |
| `POST` | `/match/optimal` | Runs the ILP solver and returns the optimal set of matched cycles |
| `POST` | `/match/greedy` | Runs the greedy baseline matcher for comparison |
| `GET` | `/benchmark` | Runs the optimal vs greedy benchmark and returns match rate and runtime results |

All five endpoints are live and have been tested through the interactive `/docs` page. Full request and response schemas are documented there automatically.

<br/>

## Benchmarks

Real numbers, produced by `python -m benchmarks.run_benchmarks`. Pool sizes were chosen because they complete a full, uncapped cycle search (no truncation, no bias), the compatibility graph gets dense fast, so larger pools are a tracked stretch goal rather than a default here, see the Roadmap.

| Pool size | Optimal matched | Greedy matched | Optimal runtime | Greedy runtime |
|---|---|---|---|---|
| 50 pairs | 18 | 15 | 19 ms | 0.1 ms |
| 100 pairs | 47 | 43 | 360 ms | 0.5 ms |
| 200 pairs | 89 | 82 | 4,272 ms | 3.0 ms |
| 300 pairs | 123 | 123 | 6,799 ms | 7.7 ms |

The optimal solver never matched fewer patients than greedy, and matched noticeably more at every pool size below 300. At 200 and 300 pairs the solver returned a strong feasible answer within its time budget rather than a formally proven optimum, worth mentioning if a judge asks, it doesn't change the result shown here, just how confidently it's labeled.

<br/>

## Screenshots

<div align="center">
<table>
<tr>
<td width="50%"><img src="docs/assets/graph-view.png" alt="Compatibility graph view" width="100%"/><p align="center"><i>Full compatibility graph, before matching</i></p></td>
<td width="50%"><img src="docs/assets/cycle-highlight.png" alt="Highlighted matched cycle" width="100%"/><p align="center"><i>A 3 way swap highlighted after matching</i></p></td>
</tr>
<tr>
<td width="50%"><img src="docs/assets/impact-dashboard.png" alt="Impact dashboard" width="100%"/><p align="center"><i>Patients matched, with versus without exchange</i></p></td>
<td width="50%"><img src="docs/assets/benchmark-chart.png" alt="Benchmark chart" width="100%"/><p align="center"><i>Optimal versus greedy, match rate and runtime</i></p></td>
</tr>
</table>
</div>

All four of these are still placeholders. Drop real screenshots into `docs/assets/` with the matching filenames and they will render automatically once pushed.

<br/>

## Roadmap

- [x] Finalize problem scope and algorithmic approach
- [x] Core data models and synthetic dataset generator
- [x] Compatibility graph construction
- [x] Bounded cycle enumeration
- [x] ILP optimal matcher
- [x] Greedy baseline matcher and benchmark suite
- [x] FastAPI backend
- [x] Interactive frontend with live cycle highlighting
- [x] Impact dashboard
- [ ] Demo gif and real screenshots in place of placeholders
- [ ] Stretch: scale cycle search past a few hundred pairs, denser pools need smarter pruning than a flat cap
- [ ] Stretch: non simultaneous extended altruistic donor chains beyond length 3
- [ ] Stretch: multi hospital pooling simulation
- [ ] Stretch: fairness aware objective, weighting rare blood types and highly sensitized patients

<br/>

## Contributing and git workflow

This project follows conventional commits, so the history itself tells the story of how it was built.

```
feat: short description of a new capability
fix: short description of a bug fix
test: short description of what is being tested
docs: short description of a documentation change
chore: short description of tooling or config work
```

Each meaningful piece of work lives on its own branch and gets merged individually, rather than as one large commit, so the commit history remains a readable record of the engineering process:

```bash
git checkout -b feat/ilp-optimal-matcher
# do the work
git add .
git commit -m "feat: add ILP formulation for optimal disjoint cycle packing"
git push origin feat/ilp-optimal-matcher
# open a pull request, merge into main
```

<br/>

## References

This project is grounded in real academic work and real production kidney exchange programs, not invented from scratch. Worth reading if you want to go deeper, or if a judge asks where the algorithm comes from.

**Academic foundations**

- Abraham, D. J., Blum, A., and Sandholm, T. (2007). *Clearing algorithms for barter exchange markets: enabling nationwide kidney exchanges.* ACM Conference on Electronic Commerce. The paper that formalized the cycle and chain clearing problem this project implements.
- Roth, A. E., Sonmez, T., and Unver, M. U. (2004). *Kidney exchange.* The Quarterly Journal of Economics. Foundational economic and mechanism design treatment of the matching problem.
- Anderson, R., Ashlagi, I., Gamarnik, D., and Roth, A. E. (2015). *Finding long chains in kidney exchange using the traveling salesman problem.* Proceedings of the National Academy of Sciences. Explains why chains, not just cycles, dominate real world matching outcomes.

**Real world programs, for grounding the numbers used in this project**

- National Kidney Registry, kidney paired donation overview and program statistics.
- United Network for Organ Sharing (UNOS), national transplant waiting list data.
- Centers for Medicare and Medicaid Services, Increasing Organ Transplant Access (IOTA) model, current waiting list and mortality figures.

**Tools used**

- [NetworkX documentation](https://networkx.org/documentation/stable/)
- [Google OR-Tools documentation](https://developers.google.com/optimization/introduction/overview)
- [FastAPI documentation](https://fastapi.tiangolo.com/)

<br/>

## Team

Built for the NSUT hackathon under the Open Innovation and Social Impact track.

| Name | Role |
|---|---|
| Jatin Solanki | Algorithm design and backend |
| Ujjawal Kumar | Frontend and visualization |
| - | Data modeling and benchmarking |

<br/>

## License

This project is released under the MIT License. See [LICENSE](./LICENSE) for the full text.

<div align="center">
<br/>
<i>If two incompatible pairs can save each other, the graph should be the one to notice.</i>
</div>
