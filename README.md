The Dream Team

## TheDreamTeam: Unit 3 Deliverable  
This project is a **Streamlit-based web application** designed to display AI-driven workout insights, user activity summaries, and motivational feedback. It integrates **Google Cloud Run** for deployment and follows best practices for **CI/CD automation** using GitHub Actions.

Important Links & Resources
- Live View of Webpage (including Community and Activities pages): https://my-ai-shoe-starter-86677331641.us-central1.run.app
- GitHub Repository: https://github.com/ISE-w-GenAI-SP25-FIU/TheDreamTeam
- Project Documentation: https://github.com/ISE-w-GenAI-SP25-FIU/TheDreamTeam/blob/main/README.md
- Google Cloud Run Guide: https://cloud.google.com/run/docs
- Deployment Workflow: https://github.com/google-github-actions/auth
- Streamlit Documentation: https://docs.streamlit.io

## Our Team

Jernai Bennett
Eric Brletic
Alain Figueroa
Euikyun Ko
Rosana Josepha

## How to run the streamlit app

### Running the Streamlit app for development

Make sure you have installed the correct packages.

```shell
$ pip install -r requirements.txt
```

Change into this directory. You can check that you're in the correct directory by running `ls`.
You should see the correct files printed out.

```shell
$ ls
app.py             data_fetcher.py       internals.py  modules_test.py  requirements.txt
custom_components  data_fetcher_test.py  modules.py    README.md        run-streamlit.sh
```

Run the following command to run the app locally. Note that if you make changes, you just
need to refresh the server and the new changes should appear (you do not need to rerun
the following command while you are actively making changes).

```shell
$ streamlit run app.py
```

### Using Docker to run the Streamlit app

Docker simply creates a virtual environment for only your app. This is what we will use to
deploy our app continuously.

Fortunately, we already have a script that builds and starts Docker for us. Run the
following command to build the container and start the server locally.

```shell
$ ./run-streamlit.sh
```

## Setting up GitHub Actions for CI/CD

The GitHub Actions are already mostly configured for you. They are split
into two files:

- `.github/workflows/cloud-run.yml`: workflow for automatic deployment
- `.github/workflows/python-checks.yml`: workflow for continuous integration (testing)

You won't need to modify `python-checks` at all, but you will need to change
the environment variables in `cloud-run.yml` to work for your team's GCP project.

### Deploy manually on the command-line

First, deploy your project manually from the command line.

1. Set up your Google Cloud Project by following the "Before you begin" section of
   http://cloud/run/docs/quickstarts/build-and-deploy/deploy-python-service?hl=en.

2. Build the image using the following command, replacing the project ID and service
   name with your info. Your service name is the name of your webapp or project and can
   be whatever you want!

```shell
gcloud builds submit --tag gcr.io/dreamteamproject-449421/my-ai-shoe-starter
```

3. Deploy the image that you just built. If successful, you should see a URL in the
   output on the command-line. Follow the link and you should see your app!

```shell
gcloud run deploy my-ai-shoe-starter \
    --image gcr.io/dreamteamproject-449421/my-ai-shoe-starter:latest \
    --region us-central1 \
    --allow-unauthenticated
```

### Set up automatic deployment in GitHub Actions

After a successful deployment, we can modify the `./github/workflows/cloud-run.yml`
file. Additional information on each step is in the [documentation](https://github.com/google-github-actions/auth?tab=readme-ov-file#workload-identity-federation-through-a-service-account)
but you should be able to follow the steps below.

1. Create a Workload Identity Pool and a Provider for GitHub. Replace `GITHUB_ORG` with the name of the GitHub org for your class. This should be before your repository name in the URL for your GitHub repository.

```shell
gcloud iam workload-identity-pools create "github" \
    --project="dreamteamproject-449421" \
    --location="global" \
    --display-name="GitHub Actions Pool"

gcloud iam workload-identity-pools providers create-oidc "project-repo" \
    --project="dreamteamproject-449421" \
    --location="global" \
    --workload-identity-pool="github" \
    --display-name="My GitHub repo Provider" \
    --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository,attribute.repository_owner=assertion.repository_owner" \
    --attribute-condition="assertion.repository_owner == 'ISE-w-GenAI-SP25-FIU'" \
    --issuer-uri="https://token.actions.githubusercontent.com"
```

3. Get the full path name for the Workload Identity Provider from gcloud.
   You will use the output from this command as the `WORKLOAD_IDENTITY_PROVIDER`
   field in `.github/workflows/cloud-run.yml`.

```shell
gcloud iam workload-identity-pools providers describe "project-repo" \
    --project="dreamteamproject-449421" \
    --location="global" \
    --workload-identity-pool="github" \
    --format="value(name)"
```

4. Authorize your service account. Use the output from the first command as the
   `WORKLOAD_IDENTITY_POOL_ID` in the second command, and your team's GitHub repo
   name as the `GITHUB_REPO_NAME`. Also replace `GITHUB_ORG` with the name of the GitHub org, same as in step 1.

```shell
gcloud iam workload-identity-pools describe "github" \
  --project="dreamteamproject-449421" \
  --location="global" \
  --format="value(name)"
```

```shell
gcloud iam service-accounts add-iam-policy-binding "86677331641-compute@developer.gserviceaccount.com" \
  --project="dreamteamproject-449421" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/86677331641/locations/global/workloadIdentityPools/github/attribute.repository/ISE-w-GenAI-SP25-FIU/TheDreamTeam"
```

4.  In IAM in the Cloud Console, double check that the following roles are attached
    to the service account.

        - Cloud Build Service Agent
        - Cloud Run Admin
        - Service Account User
        - Workload Identity User

5.  Update the environmental variables (all of the TODOs) in
    `.github/workflows/cloud-run.yml`, commit and push your changes,
    and click on "Actions" in your team's repository on GitHub to see
    the workflow running!
