"""Run with: FEEDHORIZON_API_KEY=fh_… python examples/schedule_post.py"""

from feedhorizon import FeedHorizon

client = FeedHorizon()

profile = client.profiles.list().data[0]

check = client.posts.validate(profileId=profile["id"], content="Hello from the SDK", platforms=["linkedin"], addToQueue=True)
if not check["valid"]:
    raise SystemExit(check["errors"])

post = client.posts.create(profileId=profile["id"], content="Hello from the SDK", platforms=["linkedin"], addToQueue=True)
print(f"Scheduled {post['id']} for {post['scheduledAt']}")
