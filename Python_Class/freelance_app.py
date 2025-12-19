class  User:
    def __init__(self, username, role):
        self.username = username
        self.role = role  # 'freelancer' or 'client'
        
        
class Job:
    def __init__(self, title, description, client):
        self.title = title
        self.description = description
        self.client = client
        
        self.applicants = []  # List of freelancers who applied for the job
        
    def apply(self, freelancer):
        self.applicants.append(freelancer)
    
    
class FreelancerApp:
    def __init__(self):
        self.users = []  # List of all users
        self.jobs = []   # List of all jobs
    
    def register_user(self, username, role):
        user = User(username, role)
        self.users.append(user)
        
        print(f"User {username} registered successfully as {role}.")
        
    def post_job(self, title, description, client_name):
       
        client = next((user for user in self.users if user.username == client_name and user.role == 'client'), None)
        
        if client:
            job = Job(title, description, client)
            self.jobs.append(job)
            
            print(f"Job '{title}' posted successfully.")
        
        else:
            print("client not found or not registered as a client.")
    
    def apply_to_job(self, job_title, freelancer_name):
        freelancer = next((user for user in self.users if user.username == freelancer_name and user.role == 'freelancer'), None)
        
        job = next((job for job in self.jobs if job.title == job_title), None)
        
        if freelancer and job:
            job.apply(freelancer)
            print(f"Freelancer {freelancer_name} applied for '{job_title}'.")
            
        else:
            print("Freelancer or job not found.")
            
    def list_jobs(self):
        if not self.jobs:
            print("No jobs available.")
        
        for job in self.jobs:
            print(f"Title: {job.title}, Description: {job.description}, Client: {job.client.username}, Applicants: {[f.username for f in job.applicants]}")
            
    def menu(self):
        while True:
            print("\n1. Register User\n2. Post Job\n3. Apply to Job\n4. List Jobs\n5. Exit")
        
            choice = input("Enter your choice: ")
        
            if choice == '1':
                username = input("Enter username: ")
                role = input("Enter role (freelancer/client): ")
                self.register_user(username, role)
        
            elif choice == '2':
                title = input("Enter job title: ")
                description = input("Enter job description: ")
                client_name = input("Enter client username: ")
                self.post_job(title, description, client_name)
            
            elif choice == '3':
                job_title = input("Enter job title to apply for: ")
                freelancer_name = input("Enter freelancer username: ")
                self.apply_to_job(job_title, freelancer_name)
            
            elif choice == '4':
                self.list_jobs()
                
            elif choice == '5':
                print("Exiting the application.")
                break
            else:
                print("Invalid choice. Please try again.")
            

if __name__ == "__main__":
    app = FreelancerApp()
    
    app.menu()


        
        
        

