Celery
- https://stackoverflow.com/questions/70578693/how-to-deploy-celery-worker-on-digitalocean-app-platform
-- Anytime a change is made run `sudo supervisorctl update`
-- Check status `sudo supervisorctl status`
-- Check errors `tail celery_worker stderr` (So far this doesn't work)
- Start/Stop processes: run `supervisorctl`
-- `status` to see processes
-- `start`
-- `stop`