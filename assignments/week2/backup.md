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

## 5. Real-World Consequences Applying to Others

### GitLab Database Backup Incident - 2017

In January 2017, GitLab experienced a major cloud-service outage after production database data was accidentally deleted. The company discovered that several backup and replication methods it expected to rely on were either unavailable or not functioning reliably. GitLab ultimately restored the database from a copy that was approximately six hours old, which meant that some projects, comments, user accounts, issues, and other database changes created during that period were permanently lost.

This incident could have been reduced or avoided through regularly tested backups, continuous monitoring of backup jobs, multiple independent recovery copies, and documented restoration procedures. GitLab later identified improvements such as backup monitoring, hourly snapshots, point-in-time recovery, and automated testing of database restoration procedures.

**Source:** GitLab, *Postmortem of database outage of January 31*, 2017.

## Additional Professional Example
### TV Anywhere Africa and the 2024 West African Subsea Cable Outage

One of the strongest examples of the importance of backup, redundancy, and disaster recovery comes from my own professional experience at TV Anywhere Africa in Ghana.

TV Anywhere operated IPTV platforms for major telecommunications companies across Sub-Saharan Africa. Our services depended heavily on reliable data-center infrastructure and international connectivity, with MainOne serving as our primary data-center and connectivity provider.

In March 2024, several major subsea cable systems serving Ghana and other parts of West Africa experienced simultaneous disruptions, including MainOne, WACS, ACE, and SAT-3.

The effect on our IPTV platform was significant. Because our production environment depended heavily on MainOne infrastructure, the disruption caused major service downtime. Our telecom partners also depended on our platform to deliver IPTV services to their customers, so the infrastructure failure affected services beyond our own organization.

An important lesson from the incident was that having another telecommunications provider available did not automatically provide immediate redundancy. MTN Group, one of our telecommunication partners was also affected by the wider subsea cable disruption. They are the biggest telecom network providers on the continent, so this was a major setback for all involved. The situation also demonstrated that different providers can still share the same underlying physical points of failure.

During the recovery period, MTN Group and its infrastructure operations rerouted traffic and activated alternative international capacity.

From my experience at TV Anywhere, we were eventually able to obtain additional capacity through the assistance of MTN Group. This alternative capacity allowed us to restore our systems and bring our IPTV services back online within a few days rather than waiting for MainOne's infrastructure to be completely restored.

Interestingly, MainOne's recovery took approximately eight weeks.

## Lessons Learned

The two incidents show that protecting digital systems requires more than simply creating copies of data.

The GitLab incident demonstrates that a backup is only useful if it is working, monitored, and regularly tested. An organization may believe it has a recovery plan, but failed backup jobs or untested restoration procedures can still result in permanent data loss. Multiple independent backup copies, frequent snapshots, monitoring, and periodic recovery testing can greatly reduce this risk.

My experience at TV Anywhere Africa highlighted a different but related problem. Even when data is not permanently lost, a service can still become unavailable if the infrastructure or network needed to reach that data fails. The MainOne outage showed why alternative network capacity, geographically diverse infrastructure, and tested failover procedures are important for maintaining service availability.

From these examples, I learned that an effective cloud resilience strategy should address four questions:

1. **Is the data backed up?**
2. **Can the backup actually be restored?**
3. **Can the application continue operating if the primary infrastructure fails?**
4. **How quickly can the complete service be recovered?**

This distinction helped me understand that backup, disaster recovery, and high availability are related but different concepts. Backup protects data, disaster recovery focuses on restoring systems after a failure, and high availability reduces service interruption when infrastructure fails.

## Sources

- GitLab. *Postmortem of database outage of January 31*. February 10, 2017.
- Ghana National Communications Authority. *Update 2: Undersea Cable Disruptions Affect Data Services*. March 14, 2024.
- Ghana National Communications Authority. *Update 3: Undersea Cable Disruptions Affect Data Services*. March 15, 2024.
- Bayobab Group. *Updated Statement: International Subsea Cable Break*. March 19, 2024.
- Ghana National Communications Authority. *Update 7: Repair Works on All Undersea Cable Cuts Completed as of May 8, 2024*. May 22, 2024.