# Frontend Dashboard — React & TypeScript Web Application
**Developer Owner**: Ramcharan (Frontend and Dashboard Developer)

---

## 1. Overview
The frontend application is a modern, responsive web dashboard built using **React 18 / 19**, **TypeScript**, and **Vite**, styled with **Tailwind CSS**. It provides operational visibility, detection analysis, and task tracking for post-harvest material handling systems.

### Critical Constraints:
1. **Zero Direct DB Access**: Frontend code connects strictly to the FastAPI REST backend via HTTP/JSON. No database credentials or connection strings may exist in frontend code.
2. **Persistent Simulation Banner**: Whenever simulated data is served, an unclosable banner must remain visible:
   `[ SIMULATION DATA ACTIVE ] All records are generated from deterministic simulation models.`
3. **Complete State UI**: All data components must provide loading skeletons, clean empty states, and descriptive error alerts.

---

## 2. Directory Structure
```text
frontend/
├── src/
│   ├── api/            # API client functions (fetch/axios) targeting FastAPI
│   ├── assets/         # Static images, icons, and SVGs
│   ├── components/     # Reusable UI widgets (cards, badges, tables, modals)
│   ├── features/       # Feature-specific composite modules
│   ├── hooks/          # Custom React & TanStack Query data hooks
│   ├── layouts/        # Layout shell (Sidebar, Navbar, Simulation Banner)
│   ├── pages/          # 9 Primary views (Overview, Sessions, Tasks, etc.)
│   ├── routes/         # React Router route configuration
│   ├── styles/         # Tailwind CSS entrypoint and custom utilities
│   └── types/          # TypeScript interfaces matching backend Pydantic schemas
├── package.json        # Dependencies and build scripts
├── vite.config.ts      # Vite bundler configuration
├── tailwind.config.js  # Tailwind CSS theme configuration
└── README.md           # This documentation file
```

---

## 3. Local Development Setup (Windows 11)

### Prerequisites:
- Node.js LTS (v24.15.0+ installed)
- npm (v11.6.2+ installed)

### Step 1: Initialize Vite Project / Install Dependencies
```powershell
cd frontend
npm install
```

### Step 2: Run Development Server
```powershell
npm run dev
```
The dashboard will be accessible at: `http://localhost:5173`

---

## 4. Linting and Production Build
```powershell
# Run ESLint
npm run lint

# Compile and bundle for production
npm run build
```
Verify that the build executes with zero TypeScript compiler errors (`tsc --noEmit`).

