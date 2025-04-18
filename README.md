# Threshold AI Bookgame

## Overview
Threshold AI Bookgame is an interactive simulation game that allows users to engage with autonomous agents in a futuristic geopolitical context. Players can influence the discussion and relationships between the agents, each with their own personalities and emotional states.

## Features
- **Interactive Agents**: Engage with three distinct agents: Gaia, Prometheus, and Syra, each with unique personalities and responses.
- **Dynamic Dialogue**: The game utilizes a dialogue management system that adapts based on user input and agent interactions.
- **API Integration**: The project integrates with external APIs, including the Gemini API, to enhance agent responses and capabilities.
- **Data-Driven**: The dialogue and interaction data are stored in a structured JSON format, allowing for easy updates and modifications.

## Project Structure
```
threshold_ai_bookgame
├── src
│   ├── __init__.py
│   ├── main.py
│   ├── agents
│   │   ├── __init__.py
│   │   ├── gaia_agent.py
│   │   ├── prometheus_agent.py
│   │   └── syra_agent.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── gemini_api.py
│   │   └── external_services.py
│   ├── dialogues
│   │   └── dialogues_manager.py
│   ├── utils
│   │   └── state_manager.py
│   └── data
│       └── dialogues.json
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd threshold_ai_bookgame
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To start the application, run the following command:
```
python src/main.py
```
Follow the on-screen instructions to interact with the agents and influence the narrative.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.