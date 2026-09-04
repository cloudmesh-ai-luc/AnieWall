# W2.3 - Backup Your Computer

## 1. Why Is Backing Up Important?

Backing up my computer is important because much of my academic, professional, and personal work is stored digitally. My laptop contains class assignments, programming projects, research materials, documents, and other files that would be difficult or impossible to recreate if they were lost. Hardware failure, accidental deletion, malware, software corruption, or loss of the computer could cause important work to disappear without warning. A backup provides another copy of these files that can be restored if something happens to the original system. Regular backups therefore reduce both the risk of permanent data loss and the amount of time needed to recover from an unexpected problem.


## 2. Real-World Consequences Applying to Me

Three consequences of not having a reliable backup that could directly affect me are:

1. **Loss of coursework:** I could lose completed assignments, class notes, research materials, and projects shortly before they are due.
2. **Loss of programming and technical projects:** Source code, configurations, documentation, and project files stored only on my laptop could disappear after a drive failure or accidental deletion.
3. **Loss of time and productivity:** Recreating lost academic or professional work could take many hours, and in some cases the original work may not be completely recoverable.

My previous professional experience has also shown me that backup is not only a personal-computer issue. Organizations that depend on digital systems must also plan for infrastructure failure, service outages, and disaster recovery.

## 3. Which Backup Plan Will I Use?

I will use a cloud storage service as my primary backup method because it allows important files to be stored separately from my physical computer and accessed again if the laptop is lost, damaged, or experiences a hardware failure.

My basic backup process will be:

1. Identify important folders such as coursework, documents, research files, and project folders.
2. Configure those folders to synchronize with my cloud storage account.
3. Confirm that recently modified files have synchronized successfully.
4. Organize important coursework and project files into clearly labeled folders.
5. Periodically download or restore a backed-up file to confirm that the backup is usable.

This approach gives me an off-site copy of important files and reduces the risk that a failure of my laptop will result in permanent data loss.

## 4. My Weekly Backup Schedule

I will perform a backup check every **Sunday evening at around 7:00 PM**.

During this check, I will:

- confirm that important documents and coursework have synchronized to cloud storage;
- verify that recent programming projects have been pushed to GitHub;
- check that major research and project files exist in more than one location; and
- occasionally restore or download a backed-up file to confirm that the backup is usable.

For major assignments or projects, I will also back up important changes immediately rather than waiting until the weekly schedule.

## 5. Real-World Consequences From My Professional Experience

### TV Anywhere Africa and the 2024 West African Subsea Cable Outage

One of the strongest examples of the importance of backup, redundancy, and disaster recovery comes from my own professional experience at TV Anywhere Africa in Ghana.

TV Anywhere operated IPTV platforms for major telecommunications companies across Sub-Saharan Africa. Our services depended heavily on reliable data-center infrastructure and international connectivity, with MainOne serving as our primary data-center and connectivity provider.

In March 2024, several major subsea cable systems serving Ghana and other parts of West Africa experienced simultaneous disruptions, including MainOne, WACS, ACE, and SAT-3.

The effect on our IPTV platform was significant. Because our production environment depended heavily on MainOne infrastructure, the disruption caused major service downtime. Our telecom partners also depended on our platform to deliver IPTV services to their customers, so the infrastructure failure affected services beyond our own organization.

An important lesson from the incident was that having another telecommunications provider available did not automatically provide immediate redundancy. MTN Group, one of our telecommunication partners was also affected by the wider subsea cable disruption. They are the biggest telecom network providers on the continent, so this was a major setback for all involved. The situation also demonstrated that different providers can still share the same underlying physical points of failure.

During the recovery period, MTN Group and its infrastructure operations rerouted traffic and activated alternative international capacity.

From my experience at TV Anywhere, we were eventually able to obtain additional capacity through the assistance of MTN Group. This alternative capacity allowed us to restore our systems and bring our IPTV services back online within a few days rather than waiting for MainOne's infrastructure to be completely restored.

Interestingly, MainOne's recovery took approximately eight weeks.

## What I Learned From the Incident

This experience changed how I understand backup and disaster recovery.

A traditional backup protects a copy of data, but that alone is not enough to keep a production cloud service available. An organization may still have its data and yet be unable to serve customers because the network, data center, or other infrastructure required to reach that data is unavailable.

The incident demonstrated several important principles:

- **Avoid single points of failure.** Depending heavily on one provider can cause a major outage when that provider becomes unavailable.
- **Redundancy must be physically diverse.** Two providers are not truly independent if their traffic ultimately depends on the same geographic cable routes.
- **Alternative capacity should be planned before a disaster.** Arranging emergency capacity during an active outage takes time.
- **Backups must include service recovery.** Organizations should plan not only how to recover data, but also how to restore applications, networking, and customer access.
- **Failover procedures must be tested.** A secondary data center, cloud environment, or network route is most useful when an organization already knows how to move production services to it.

A stronger architecture would therefore include geographically separated backups, replication to a secondary environment, independent network paths, alternative providers, and a tested disaster-recovery procedure.

The incident showed me personally that resilience in cloud computing is not simply about asking, **"Do we have a backup?"** A more important question is, **"If our primary environment fails today, how quickly can we restore the complete service somewhere else?"**

## Sources

- Ghana National Communications Authority, updates on the March 2024 undersea cable disruptions.
- MTN Group / Bayobab, updates on restoration and alternative international capacity during the March 2024 outage.