# Engineering Ladder Assessment Tool

A Python-based self-assessment tool that generates visual radar charts for engineering ladder evaluations. This tool
helps engineers and engineering managers assess skills across five key dimensions commonly used in engineering career
progression frameworks.

For the original framework refer to the awesome page https://www.engineeringladders.com/

## 🎯 Features

- **Interactive Assessment**: Rate yourself across 5 key engineering dimensions
- **Visual Radar Chart**: Generate professional-looking spider/radar charts
- **Level Assessment**: Get an approximate level (Junior, Mid-Level, Senior, etc.) based on your scores
- **Customizable Output**: Save charts as high-resolution PNG images

## 📊 Assessment Dimensions

The tool evaluates you across five key areas:

### 1. **Technology**

- **Adopts**: Actively learns and adopts new technologies
- **Specializes**: Develops deep expertise in specific technologies
- **Evangelizes**: Shares knowledge and promotes best practices
- **Masters**: Recognized expert with advanced knowledge
- **Creates**: Invents new technologies or significantly contributes to existing ones

### 2. **System**

- **Enhances**: Enhances and improves existing systems
- **Designs**: Designs and implements systems within requirements
- **Owns**: Takes ownership of system components and evolution
- **Evolves**: Drives system evolution and architectural improvements
- **Leads**: Leads system architecture across multiple teams

### 3. **People**

- **Learns**: Learns from team members and receives guidance
- **Supports**: Provides support and guidance to team members
- **Mentors**: Actively mentors and develops other engineers
- **Coordinates**: Coordinates across teams and stakeholders
- **Manages**: Manages people and teams effectively

### 4. **Process**

- **Follows**: Follows established processes and procedures
- **Enforces**: Ensures team adherence to processes
- **Challenges**: Questions and improves existing processes
- **Adjusts**: Adapts processes to team and project needs
- **Defines**: Creates and defines new processes

### 5. **Influence**

- **Subsystem**: Influences technical decisions within a subsystem
- **Team**: Influences technical decisions across the team
- **Multiple Teams**: Influences technical decisions across multiple teams
- **Company**: Influences technical decisions across the company
- **Community**: Influences technical decisions in the broader community

## 🚀 Installation

### Prerequisites

- Python 3.11 or higher
- [Poetry](https://python-poetry.org/) package manager

### Install with Poetry

```bash
poetry install
```

## 🎮 Usage

Run the assessment:

```bash
poetry run engineering-ladder
```

Or alternatively:

```bash
poetry run python main.py
```

## 📈 Level Assessment

Based on your average score across all dimensions, the tool provides an approximate engineering level:

| Average Score | Level |
|--------------|-------|
| 1.0 - 1.4 | Junior |
| 1.5 - 2.4 | Junior-ish |
| 2.5 - 2.9 | Mid-Level |
| 3.0 - 3.4 | Mid-Level-ish |
| 3.5 - 3.9 | Senior |
| 4.0 - 4.4 | Senior-ish |
| 4.5 - 5.0 | Staff/Principal |

The level is displayed both in the terminal output and on the generated radar chart.

## 📄 License

MIT