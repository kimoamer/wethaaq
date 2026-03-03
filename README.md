# 📚 Wethaaq (Contracts) - Official HR User Guide

Welcome to **Wethaaq**, the internal Legal & HR Contract Lifecycle Management system seamlessly integrated with your Frappe HRMS. Wethaaq allows HR teams to build, manage, dynamically track, securely send for e-signature, and store employee contracts with built-in legal safeguards to protect the organization.

---

## 🚀 Installation & Setup

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app wethaaq
```

---

## 🔄 The Wethaaq Contract Lifecycle (At a Glance)

Before diving into the setup, here's a bird's-eye view of how a contract moves through the system from creation to autopilot management:

```text
 ┌────────────────┐         ┌────────────────────┐
 │ Clause Library │         │ Contract Templates │
 └───────┬────────┘         └─────────┬──────────┘
         │                            │
         └─────────────┐  ┌───────────┘
                       ▼  ▼
            ╭──────────────────────╮
            │  1. Draft Contract   │
            ╰──────────┬───────────╯
                       │  Submit for Approval
                       ▼
            ╭──────────────────────╮
            │  2. Under Review     │
            ╰──────────┬───────────╯
                       │  Send for E-Signature
                       ▼
            ┏━━━━━━━━━━━━━━━━━━━━━━┓
            ┃  3. e-Signature Link ┃━━━━━━┓
            ┗━━━━━━━━━━┳━━━━━━━━━━━┛      ┃
                       │                  ▼
                       │        [ 🔒 SHA-256 Hash ]
                       │        (Locks Doc History)
                       │                  ┃
                       │  Signed by Emp   ┃
                       ▼                  ┃
            ╭──────────────────────╮      ┃
            │  4. Signed Contract  │◀━━━━━┛
            ╰──────────┬───────────╯
                       │  Mark as Active (HR)
                       ▼
            ╭──────────────────────╮
            │  5. Active Contract  │
            ╰──────────┬───────────╯
                       │  Time Passes
                       ▼
                 { 30 Days to }
                 {   Expiry?  }
                       │
          ┌────────────┴────────────┐
         Yes                        No
          │                          │
          ▼                          ▼
    ┏━━━━━━━━━━━┓           ╭────────────────╮
    ┃ Autopilot ┃           │ Remains Active │
    ┗━━━━━┳━━━━━┛           ╰────────────────╯
          │
      ┌───┴───┐
      ▼       ▼
 [ Email ] [ ToDo ]
  Alerts    Tasks
```

---

## 🧭 1. Navigating to Wethaaq
Wethaaq is embedded right where you already work. 
1. Log in to the desk interface.
2. Open the **HR** module. 
3. Look for the **Wethaaq (Contracts)** workspace. This is your central hub for drafting contracts, managing templates, and handling clause libraries.

---

## 🧱 2. Setting Up Your Building Blocks (Templates & Clauses)
Before creating a contract for a specific employee, you can define standardized corporate templates and clauses to save time.

### A. Wethaaq Clause (The Library)
Use **Clauses** to store standard legal terminology (e.g., *Confidentiality Agreement, Non-Compete, Standard Working Hours*).
- Navigate to **Wethaaq Clause** and click **Add**.
- Give the clause a distinct title and type out the legal text. 
- **Pro-tip:** By splitting legal text into separate clauses, you can pull different clauses into different employee contracts without rewriting them! These act as auto-numbered appendices in the final print.

### B. Wethaaq Contract Template
Use **Templates** to standardize contract formats for specific employment categories.
- Navigate to **Wethaaq Contract Template** and click **Add**.
- Set the **Template Name** (e.g., "Standard Fixed-Term Junior").
- Set the **Contract Type** (Fixed, Open, Intern, etc.).
- The **Content** section uses Jinja variables (like `{{ doc.employee_name }}`) to dynamically inject data into the printed agreement. When constructing actual employment agreements, Wethaaq will automatically fetch this layout for you.

---

## 📝 3. Creating a New Employee Contract
When you are ready to formally hire or renew an employee, generate a secure contract record.

1. Go to **Wethaaq Contract** and click **Add**.
2. **Select the Employee:** 
   * *Smart Safeguard:* The system only allows you to select **Active** employees! If someone was terminated, they will not appear in the dropdown. 
   * *Auto-Fetch:* Selecting an ID automatically pulls their **Name**, **Company**, and **Department** directly into the form.
3. **Select Contract Type & Template:** 
   * *Smart Safeguard:* If you select "Fixed" as the Contract Type, the Template dropdown will automatically filter out incompatible templates, preventing legal mismatches. 
4. **Financial & Dates:** Set the **Start/End Dates**, base **Currency**, and **Basic Salary**.
5. **Appendices:** Add standard corporate **Clauses** directly to the bottom of the form via the table. 
6. Click **Save**. The contract is now securely stored in **Draft** status.

---

## 🔄 4. The Signing & Active Lifecycle
Wethaaq enforces strict document tracking states. You can push a contract through its natural lifecycle using the buttons at the top right of the screen.

### 🟡 Draft ➔ Review
When HR has drafted the contract, you can submit it to "Review" so legal or senior leadership can audit the salary, company assignment, and clauses.

### 🖨️ Generate PDF Print Format
At any time, you can generate a legally formatting document:
- Click the **Print** icon at the top of the record.
- The **Wethaaq Contract Default Form** will merge the Employee data, Template Content, Appendices, and sign-off blocks into a highly optimized, multi-page layout appropriate for physical signing or legal storage.

### 🟣 Send for E-Signature (Direct Portal)
Once the review is complete, click **Send for E-Signature**.
- **What happens:** The system locks the contract and generates a unique, cryptographic **Content Hash** (SHA-256). An email is dispatched automatically to the employee containing a secure link to the Wethaaq E-Signature portal. The status changes to **Signed**.
- **The Employee Portal:** The employee clicks the link (which is securely authenticated using their document hash token) and uses the digital Signature Pad embedded in the document to sign their name from any Mobile or Desktop browser context.
- **Why it matters:** This strict mathematical security hash permanently locks the employee, salary, dates, and clauses limitlessly protecting against tampering, natively complying with ISO 15489 standards for digital evidence! 

### 🟢 Mark as Active
Once the employee actually signs the document, their signature is mapped directly into Frappe database. HR can then open the contract and manually click **Mark as Active**. The contract is now officially enforcing employment!

### 🔴 Terminations
If an employee leaves or a contract is canceled prematurely, click **Terminate Contract**. Wethaaq will prompt you to provide a definitive **Termination Date** (preventing retro-active terminations ahead of start dates) and a documented **Reason for Termination**. It permanently locks the record to ensure strict historical audits.

---

## 📊 5. Visual Board Tracking
Inside the list view and the forms, every contract is distinctly color coded:
* 🟢 **Active:** Green
* 🔵 **Signed:** Blue
* 🟡 **Review:** Orange
* ⚫ **Draft:** Grey
* 🔴 **Expired:** Red
* ⚪ **Terminated:** Dark Grey

---

## ⏰ 6. Automated Alerts & Expirations (Autopilot)
You never have to worry about missing an expiration date. Wethaaq works in the background while you sleep!

- **The 30-Day Radar:** Every single night, the server scans all contracts sitting in the **Active** status. 
- **Automated Emails:** If an employee's `End Date` is exactly **30 days away**, Wethaaq automatically dispatches a high-priority warning email to anyone holding the **HR Manager** system role.
- **Automated ToDo Generation:** Concurrently, Wethaaq generates an open system **ToDo** task pinned directly to the HR Manager's desk reminding them to either *Renew* or *Terminate* the contract before the time expires. Duplicates are strictly guarded against.

---

## 🔐 7. Privacy & Security Built-in
- **Row-Level Department Protection:** Standard `HR Users` can only view and manage contracts for employees in their own specific `Department`. They cannot see executive or cross-department contracts. Full access requires the `HR Manager` role.
- **Library Protection:** HR Users cannot delete core Clauses or Templates, ensuring the structural foundations remain stable across the entire company.
- **Guest E-Sign:** E-signatures strictly operate entirely outside the system environment — allowing the employee to safely execute a contract without requiring an entire active Frappe portal session inside the HR app.

> **Correction or Renewal Note:** If there is a mistake in an active contract, you can always hit the **Amend** button at the top right to generate a pristine, legally trackable Version 2 (`-1`) of the contract while freezing the original history.

---

### Contributing & Code Validation

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/wethaaq
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:
- ruff
- eslint
- prettier
- pyupgrade

### License
MIT
