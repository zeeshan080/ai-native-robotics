# Allowed Technologies

## Backend Stack

| Category | Allowed | NOT Allowed |
|----------|---------|-------------|
| Web Framework | FastAPI | Django, Flask, Express, Nest.js |
| Vector Database | Qdrant | Pinecone, Weaviate, Milvus |
| Authentication | BetterAuth | Passport, Auth0, Firebase Auth |
| ORM | SQLAlchemy (if needed) | Prisma, TypeORM |
| Language | Python 3.11+ | Node.js for backend |

## Frontend Stack

| Category | Allowed | NOT Allowed |
|----------|---------|-------------|
| Static Site | Docusaurus 3.x | Next.js, Gatsby, Hugo |
| UI Framework | React 18+ | Vue, Angular, Svelte |
| Language | TypeScript | JavaScript (prefer TS) |
| Styling | CSS Modules, Tailwind | Styled Components, Emotion |
| Chatbot | CopilotKit/ChatKit | Custom chatbot |

## Robotics Stack

| Category | Allowed | NOT Allowed |
|----------|---------|-------------|
| Middleware | ROS 2 Humble | ROS 1, custom middleware |
| Simulation | Gazebo, Isaac Sim | Unity, Unreal (for robotics) |
| Robot Description | URDF, XACRO | SDF (prefer URDF) |
| Message Format | ROS 2 standard msgs | Custom protocols |

## Infrastructure

| Category | Allowed | NOT Allowed |
|----------|---------|-------------|
| Static Hosting | GitHub Pages | Vercel, Netlify |
| API Hosting | Cloud Run, Railway | AWS Lambda, Heroku |
| CI/CD | GitHub Actions | Jenkins, CircleCI |
| Secrets | .env files, GitHub Secrets | Hardcoded values |

## Python Dependencies

```txt
# Backend
fastapi>=0.100.0
qdrant-client>=1.7.0
pydantic>=2.0.0
uvicorn>=0.24.0

# Robotics Content
# (no Python packages - URDF/ROS content only)
```

## Node.js Dependencies

```json
{
  "dependencies": {
    "@docusaurus/core": "^3.0.0",
    "react": "^18.2.0",
    "typescript": "^5.0.0"
  }
}
```
