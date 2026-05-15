# Security

This repository currently runs local camera inference and writes local output files. It does not intentionally expose a public service yet.

## Sensitive Data

Possible sensitive data:

- GPS coordinates
- Captured images
- Drone routes
- Local machine paths
- API keys if future dashboard services are added

Do not commit:

- `.env`
- API keys
- private GPS logs
- personally sensitive field images
- generated `runs/` folders

## Camera And Location Safety

When testing with DroidCam or drone footage:

- Avoid recording people without consent.
- Avoid exposing exact sensitive locations in public demos.
- Use sample coordinates for screenshots and teaching materials when possible.

## Future Dashboard Security

When the dashboard gets a backend:

- Store secrets in environment variables.
- Validate uploaded image paths.
- Never let API callers read arbitrary local files.
- Add authentication before exposing data outside localhost.
- Consider role-based access for field operators and researchers.

## Reporting Issues

For now, record security concerns as repository issues or in a private project note, depending on sensitivity.

