# Project Proposal - Cloud-Native Biometric Consent and Audit Platform

**Student:** Stephanie Wallace  
**Loyola Email:** swallace6@luc.edu  
**GitHub ID:** AnieWall  
**Course:** Cloud Computing, DevOps, and AI  
**Instructor:** Gregor von Laszewski  
**Date:** September 8, 2026  
**Status:** Initial Proposal  

---

## Working Title

**Cloud-Native Biometric Consent and Audit Platform**

---

## Project Description

Biometric technologies such as facial-recognition systems can process sensitive personal information. Before biometric information is collected or used, an application may need to determine whether valid consent exists, what purpose the consent covers, whether the consent is still active, and whether it has been revoked.

My previous academic work explored the design of biometric consent mechanisms, including consent capture, verification, revocation, and auditability.

For this Cloud Computing project, I want to investigate a different technical problem:

**How can a biometric-consent mechanism be deployed, secured, monitored, and operated as a cloud service?**

The proposed project will create a small cloud-hosted consent-verification service. A client application will send a request asking whether a simulated biometric operation is permitted. The service will check the applicable consent record and return an `allow` or `deny` result.

Each verification or revocation event will also be recorded so that activity can later be audited.

The prototype will use synthetic identifiers and simulated consent records. It will not collect or process real biometric information.

---

## Problem and Motivation

Consent may be implemented directly inside an individual application. However, this can make it difficult to reuse the consent mechanism across multiple systems or to manage important cloud-computing concerns such as:

- availability;
- security;
- monitoring;
- persistent storage;
- backup and recovery;
- auditability;
- service deployment; and
- controlled access.

A separate cloud-hosted consent service could allow multiple applications to verify consent through a common interface.

For example, before performing a simulated facial-verification operation, an application could ask:

> Does this user currently have valid consent for this specific purpose?

The cloud service would evaluate the stored consent information and return a decision.

---

## Proposed Cloud Solution

The initial system will contain several basic components.

### Client / Demo Application

A simple client will submit requests to the consent service.

The client may request permission for a simulated biometric operation such as:

- identity verification;
- account authentication; or
- another predefined purpose.

### Consent Verification API

A REST API will receive requests from the client.

The API will:

1. identify the relevant consent record;
2. determine whether the requested purpose is permitted;
3. determine whether the consent is active or revoked;
4. return an `allow` or `deny` response; and
5. record the decision.

### Consent Data Store

The system will maintain synthetic consent information such as:

- consent identifier;
- synthetic user identifier;
- permitted purpose;
- consent status;
- date granted; and
- date revoked.

### Audit Log

The audit component will record important events such as:

- consent creation;
- consent verification;
- successful authorization;
- denied requests; and
- consent revocation.

### Cloud Environment

The first version of the service is expected to run on an Ubuntu virtual machine in **Chameleon Cloud**.

---

## Initial Architecture

```text
                 +------------------------+
                 |   Client / Demo App    |
                 +-----------+------------+
                             |
                             | HTTPS / REST
                             |
                             v
                 +------------------------+
                 | Consent Verification   |
                 |      REST API          |
                 |       FastAPI          |
                 +-----------+------------+
                             |
                    +--------+--------+
                    |                 |
                    v                 v
          +------------------+   +------------------+
          | Consent Data     |   | Audit Log        |
          | Store            |   |                  |
          +------------------+   +------------------+

                    Application hosted on

                 +------------------------+
                 | Chameleon Cloud VM     |
                 | Ubuntu Linux           |
                 +------------------------+

                             ^
                             |
                     GitHub / DevOps
```

This architecture is preliminary and may change as the project develops and additional cloud-computing topics are introduced in the course.

---

## Initial Technology Ideas

The exact technologies have not yet been finalized.

| Component | Initial Idea |
| --- | --- |
| Cloud platform | Chameleon Cloud |
| Operating system | Ubuntu Linux |
| Application language | Python |
| REST API | FastAPI |
| Initial database | SQLite |
| Later database option | PostgreSQL |
| Version control | GitHub |
| API testing | curl / Postman |
| Monitoring | Application and Linux logs |
| Containerization | Docker, if appropriate later |
| CI/CD | GitHub Actions, if appropriate later |

The project will begin with the smallest functional implementation and become more advanced as relevant topics are covered in class.

---

## Privacy and Security Considerations

Privacy is an important part of this project because the system represents consent associated with biometric-data use.

The prototype will therefore consider principles such as:

- **data minimization** - store only the information necessary for the demonstration;
- **purpose limitation** - associate consent with a specific approved use;
- **least-privilege access** - restrict access to consent information;
- **encryption in transit** - protect API communication where practical;
- **audit logging** - maintain records of important actions and decisions;
- **secrets management** - avoid placing passwords, tokens, or private keys in GitHub;
- **backup and recovery** - determine how persistent consent records could be restored; and
- **revocation** - ensure that revoked consent no longer authorizes subsequent requests.

The prototype will use synthetic information rather than real biometric data.

---

## Relationship to My Previous Biometric Project

This project is related to my previous research topic but has a different technical objective.

My earlier biometric project concentrated primarily on questions such as:

- how biometric consent should be represented;
- how consent should be captured;
- how consent can be verified;
- how consent can be revoked;
- how activity can be audited; and
- how legal and regulatory requirements influence consent design.

The Cloud Computing project will instead concentrate on how such a mechanism can be implemented and operated as a cloud service.

The new technical focus includes:

- cloud virtual machines;
- Linux deployment;
- REST APIs;
- persistent storage;
- networking;
- service availability;
- security configuration;
- monitoring;
- backup and recovery; and
- DevOps practices.

Therefore, the intention is not to reproduce the previous project, but to use its problem domain as the basis for a new cloud-systems implementation.

---

## Possible AI Extension

A later phase of the project may explore an AI component.

For example, an LLM could potentially assist with converting human-readable consent language into structured consent attributes.

Example:

```text
Human-readable consent:

"I agree to facial verification for account login,
but I do not agree to its use for advertising."
```

The AI component could assist in identifying structured information such as:

```text
Purpose: authentication
Authentication allowed: yes
Advertising allowed: no
```

The final `allow` or `deny` decision would remain rule-based rather than being determined directly by the LLM.

This AI component is currently an optional extension and is not required for the first prototype.

---

## Initial Goals

At this stage, I expect the project to demonstrate that:

1. a consent record can be created using synthetic data;
2. a client can request consent verification;
3. the service can return an `allow` or `deny` result;
4. consent can be revoked;
5. a request after revocation can be denied;
6. important events can be recorded in an audit log; and
7. the service can run in a cloud-hosted Ubuntu environment.

These goals may be refined as the project develops.

---

## Scope

### Initially In Scope

- Cloud deployment
- Consent verification
- Synthetic consent records
- REST API
- Consent revocation
- Audit logging
- Basic persistence
- Security configuration
- Monitoring
- Backup and recovery
- Documentation

### Currently Out of Scope

- Collection of real biometric data
- Training facial-recognition models
- Real-world biometric identification
- Production use
- Enterprise-scale deployment
- Full compliance certification
- Repeating the complete legal analysis from my previous project

---

## Next Steps

The next stages of the project will include:

1. reviewing the proposed architecture with the instructor;
2. refining the project scope;
3. determining the initial Chameleon Cloud configuration;
4. designing the basic consent data model;
5. defining the first REST API operations;
6. deploying a minimal application to an Ubuntu cloud VM;
7. refining security and privacy requirements; and
8. determining which DevOps and AI components are appropriate as the course progresses.

---

## Relevant Course Resources

- Cloud Computing Introduction:  
  https://cloudmesh-ai.github.io/cloudmesh-ai-lecture/lecture/cloud/introduction/

- Virtualization Lecture:  
  https://cloudmesh-ai.github.io/cloudmesh-ai-lecture/lecture/cloud/virtualization/

- Privacy Lecture:  
  https://cloudmesh-ai.github.io/cloudmesh-ai-lecture/section/cloud/privacy/

---

## Current Status

This is an initial project proposal.

The architecture, technology choices, AI component, deployment strategy, and evaluation criteria are expected to evolve during the semester based on course material, implementation experience, and instructor feedback.