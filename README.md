# 🤖 AI Job Application Agent

An automated AI agent that searches for and applies to jobs on LinkedIn, specifically targeting **Fresher**, **Internship**, and **Entry Level** roles for Data Science and AI/ML positions.

Built with **Python**, **Playwright**, and **Streamlit**.

## 🚀 Features

- **Automated Search**: Scrapes LinkedIn for jobs matching your keywords and location.
- **Fresher Focused**: Strictly filters for 0-1 years experience (Internship/Entry Level).
- **Easy Apply**: Attempts to automate the "Easy Apply" process on LinkedIn.
- **Web Interface**: User-friendly dashboard built with Streamlit.
- **Session Persistence**: Remembers your login session so you don't have to log in every time.
- **Multi-Location**: Searches across multiple locations (e.g., Hyderabad, Bangalore, Pune, Remote).

## 🛠️ Prerequisites

- **Python 3.8+** installed.
- **Google Chrome** browser installed.
- **LinkedIn Account**.

## 📥 Installation

1.  **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd <repo-name>
    ```

2.  **Install Python dependencies**:
    ```bash
    pip install -r job_agent/requirements.txt
    ```

3.  **Install Playwright browsers**:
    ```bash
    playwright install
    ```

## ⚙️ Configuration

1.  **Resume**: Place your resume PDF file named `resume.pdf` in the root directory of the project.
2.  **Credentials**:
    - Create a file named `.env` inside the `job_agent` folder.
    - Add your LinkedIn credentials:
      ```env
      LINKEDIN_USERNAME=your_phone_or_email
      LINKEDIN_PASSWORD=your_password
      ```

## 🖥️ Usage

1.  **Run the Web Interface**:
    ```bash
    streamlit run app.py
    ```

2.  **Interact with the App**:
    - The app will open in your browser.
    - **Search Jobs**: Click the button to find jobs.
    - **Apply**: Click "Apply to All" to start the application process.

> **Note**: On the first run, you might need to manually solve a CAPTCHA or enter an OTP in the opened Chrome window. The agent will remember your session for next time.

## ⚠️ Disclaimer

**Use with Caution**: Automated scraping and applying may violate LinkedIn's Terms of Service. This tool is for educational purposes. The author is not responsible for any account restrictions or bans. Use at your own risk.
