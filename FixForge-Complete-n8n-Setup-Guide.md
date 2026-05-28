# The Complete FixForge n8n Automation Guide (V2)

This guide covers everything you need to get your fully automated Prompt Analysis email pipeline up and running, including the new dynamic HTML emails and PDF attachments.

---

## 🛠️ Step 1: Prepare Your Email (Gmail Example)
To allow n8n to read and send emails, you need an "App Password" (if you use Gmail or Outlook).

1. Go to your **Google Account settings** -> **Security**.
2. Ensure **2-Step Verification** is turned on.
3. Search for **App Passwords** in the search bar.
4. Create a new App Password (name it "n8n FixForge").
5. **Copy the 16-character password** generated. You will need this for n8n.

---

## 🐍 Step 2: Restart the FixForge Backend
Because I added a brand new `/api/generate-pdf` endpoint to your backend to handle PDF creation, you must restart your Python server to apply the changes.

1. Open your terminal or command prompt.
2. Navigate to your project folder:
   ```bash
   cd c:\Users\ASUS\OneDrive\Desktop\FixForge
   ```
3. Stop any running backend servers (press `Ctrl + C`).
4. Start the backend again:
   ```bash
   cd backend
   uvicorn app:app --reload --port 8000
   ```
5. Leave this terminal window open so the API stays active.

---

## 📥 Step 3: Import the Workflow into n8n
1. Open your n8n interface (usually `http://localhost:5678`).
2. Go to **Workflows** on the left menu and click **Add Workflow**.
3. In the top right corner, click the three dots (`...`) menu.
4. Select **Import from File...**
5. Locate and open the `n8n_workflow_v2.json` file located at:
   `c:\Users\ASUS\OneDrive\Desktop\FixForge\n8n_workflow_v2.json`

---

## ⚙️ Step 4: Configure the n8n Nodes

Now that the workflow is imported, you will see 5 nodes. Let's configure them left-to-right.

### Node 1: "Watch Email Inbox"
1. Double-click the node.
2. Click **Create New Credential** -> **IMAP**.
3. Enter your details:
   - **User**: Your email address (e.g., `you@gmail.com`)
   - **Password**: The **16-character App Password** from Step 1.
   - **Host**: `imap.gmail.com`
   - **Port**: `993`
   - **SSL/TLS**: On
4. Save the credential.
5. Close the node. (Leave `Download Attachments` set to true).

### Node 2: "Check for .md or .txt"
- **No changes needed.** This node automatically filters out emails without markdown or text file attachments to prevent errors.

### Node 3: "FixForge API Analysis"
- **No changes needed.** This node automatically takes the `.md` or `.txt` attachment and sends it to `http://localhost:8000/api/analyze/file`.

### Node 4: "Generate PDF Report"
- **No changes needed.** This node automatically takes the JSON response from Node 3 and sends it to `http://localhost:8000/api/generate-pdf` to get the PDF file binary.

### Node 5: "Send Reply Email"
1. Double-click the node.
2. Click **Create New Credential** -> **SMTP**.
3. Enter your details:
   - **User**: Your email address (e.g., `you@gmail.com`)
   - **Password**: The **same 16-character App Password** from Step 1.
   - **Host**: `smtp.gmail.com`
   - **Port**: `465`
   - **SSL/TLS**: On
4. Save the credential.
5. In the node settings, update the **From Email** field to exactly match your email address (e.g., `you@gmail.com`).
6. **No other changes needed.** The To Email, Subject, HTML Body, and PDF Attachment are all dynamically mapped for you!

---

## 🚀 Step 5: Test the Pipeline
1. At the bottom of the n8n screen, click the **Test Workflow** button.
2. Open your personal email (a different account, or your phone) and send a new email to the account n8n is watching.
3. **Attach a `.md` or `.txt` file** containing a prompt to the email. (The subject and body don't matter).
4. Watch the n8n canvas! You will see green checkmarks appear on each node as it processes the email.
5. Check your inbox: You will receive an automated reply containing the dynamic HTML score table and the `report.pdf` attachment.
6. If everything works perfectly, toggle the **Active** switch in the top right corner of n8n to let it run automatically in the background forever!
