JobQuest is a web-based job application tracking and ATS resume analysis platform developed using Python, Streamlit, and SQLite. The primary goal of this project is to help students and job seekers manage their entire job application process in one centralized system. Instead of maintaining spreadsheets or notes, users can store job applications, analyze resumes against job descriptions, and track their progress efficiently through a simple and fast web interface.

## 🚀 Features
- Secure user authentication (Login / Signup)
- Job application tracking with status updates
- ATS resume analyzer using keyword matching
- Resume vs Job Description comparison
- SQLite database for persistent storage
- Clean and fast Streamlit UI


The application provides a secure authentication system that includes login, signup, password hashing using SHA-256, CAPTCHA verification, and session-based access control. Each user has a protected session, ensuring that personal data such as job applications and resume analysis reports remain private and accessible only to the logged-in user. A forgot password feature is implemented where password reset requests are sent to the admin for approval, adding an extra layer of security.

One of the core features of JobQuest is the Job Application Tracker. Users can record job applications from different platforms such as LinkedIn, Naukri, company career pages, or referrals. For each application, details like company name, job role, location, application date, status, source, and personal notes are stored in the database. Users can view, manage, and delete applications easily, helping them stay organized throughout their job search journey.

Another major component of the project is the ATS Resume Analyzer. Users upload their resume in PDF format and paste a job description. The system extracts text from the resume, identifies relevant skills using keyword matching and regular expressions, and compares them with the skills found in the job description. Based on this comparison, an ATS compatibility score is calculated and displayed. The analyzer also shows matched skills, missing skills, and improvement suggestions to help users optimize their resumes. Each analysis result is saved in the database for future reference.

JobQuest also includes a User Dashboard that provides an overview of the user’s activity. It displays metrics such as the total number of job applications submitted and the number of ATS resume analyses performed. Recent activities are shown to give users quick insights into their progress. The dashboard is designed with a clean and minimal user interface to ensure a smooth user experience.

An Admin Dashboard is implemented with role-based access control. Only users with the admin role can access this section. The admin dashboard allows monitoring of the total number of registered users and management of password reset requests. Admins can approve or reject reset requests, ensuring that sensitive operations are handled securely. This separation of user and admin roles demonstrates proper access control and real-world system design.

The project uses SQLite as the database, making it lightweight and easy to manage without requiring a separate server. Multiple tables are designed to handle users, job applications, ATS reports, and password reset requests. All database operations are performed securely with parameterized queries to prevent SQL injection risks.

JobQuest is intentionally built using Streamlit to enable rapid development and deployment. Streamlit allows quick UI creation with Python while maintaining readability and simplicity. This makes the project ideal for academic submissions, portfolio demonstrations, and interview discussions.

Overall, JobQuest is a real-world, end-to-end application that demonstrates practical knowledge of Python programming, database management, authentication systems, and user-centric design. It is especially useful for students and freshers preparing for placements, as it addresses common job search challenges while showcasing strong software development fundamentals.

## 🔮 Future Enhancements
- Email notifications
- Admin dashboard
- Resume recommendations
- Cloud database integration

