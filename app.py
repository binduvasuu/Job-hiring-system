from flask import Flask, render_template, request, redirect
import json
import time

app = Flask(__name__)

def load_jobs():
    try:
        with open("jobs.json", "r") as f:
            return json.load(f)
    except:
        return []

def save_jobs(jobs):
    with open("jobs.json", "w") as f:
        json.dump(jobs, f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/jobs")
def jobs():
    job_list = load_jobs()
    return render_template("jobs.html", jobs=job_list)

@app.route("/post-job", methods=["GET", "POST"])
def post_job():
    if request.method == "POST":
        job = {
            "id": str(time.time()),  # This is the ID we're talking about
            "title": request.form["title"],
            "company": request.form["company"],
            "location": request.form["location"],
            "desc": request.form["desc"]
        }
        job_list = load_jobs()
        job_list.append(job)
        save_jobs(job_list)
        return redirect("/jobs")
    return render_template("post_job.html")

@app.route("/apply")
def apply():
    return render_template("apply.html")

if __name__ == "__main__":
    print("Flask server is starting...")
    app.run(debug=True)

@app.route("/delete-job/<job_id>", methods=["POST"])
def delete_job(job_id):
    jobs = load_jobs()
    updated_jobs = [job for job in jobs if job["id"] != job_id]
    save_jobs(updated_jobs)
    return redirect("/jobs")
