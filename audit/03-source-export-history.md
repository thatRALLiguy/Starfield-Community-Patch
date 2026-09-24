# Why the four weapon records are missing from GitHub

Checked: 2026-09-23. Scope: repository history and release metadata, not a full patch audit.

## Confirmed cause of the source/changelog mismatch

Release verification completed in audit 04: the user-supplied SFCP 1.0.0 ESM contains all four records. Their keyword arrays match the supplied USFP 1.1.0 ESM. The GitHub omission is not a missing-record defect in this downloaded SFCP release.

The serialized plugin records in spriggit were not updated alongside the September 2024 changelog and assets. Upstream main and the user's fork point to 0ad97d3eb087dafb91afbc4bbb1588598212cc87. This is an upstream condition, not a fork-copy failure.

The entire spriggit directory has tree SHA fad6dcc0d7a82dc4f65f18704957f08dadc75ccb at both:

- June 17, 2024 export commit 8d922b42bef4b38c166173b89d9588a90a09b970.
- Current main, 0ad97d3eb087dafb91afbc4bbb1588598212cc87.

Identical tree hashes establish that all tracked paths and file contents in this directory are unchanged between these snapshots. The history for spriggit and spriggit/Weapons also identifies June 17 as the most recent change.

The September 30 commit eaeb24a6909f4c3a4028433a57ff0a2786fde7cc, titled Update 1.0.0, changes 13 files: the changelog, ten script source files, and two meshes. It contains no spriggit update. The four weapon keyword fixes are documented in that newer changelog, but the tracked plugin export remains the June snapshot.

## Historical context, not a proven explanation for the later omission

A May 18 commit explicitly reports that a new form type prevented a full conversion. June then contains a Spriggit 0.23 export. GitHub release metadata also includes assets labeled No.Spriggit for 0.1.3 and 0.1.6. These establish prior conversion/workflow difficulties; they do not establish why exports stopped after June, or prove that the June export was complete.

The related melee-weapon PR 1045 was closed without merging, with a maintainer comment saying its fixes would be included in 0.1.8. The 1.0.0 changelog later credits those fixes. This is consistent with release changes being incorporated outside the tracked YAML workflow, but the released ESM must be inspected to verify its actual contents.

## Consequence

Do not reconstruct missing fixes from the changelog yet. A build using the checked-in workflow's spriggit input uses the older record snapshot alongside newer assets. This source tree is not established as a reproducible representation of the documented 1.0.0 release.

Next small step: obtain the official distributed 1.0.0 ESM and inspect only Grendel, Kodama, Shotty, and Maelstrom. If those fixes are present there, use that released plugin to recover and validate the source baseline before changing gameplay records. This audit does not claim the released patch lacks the fixes.

## Sources

- [June export](https://github.com/Starfield-Community-Patch/Starfield-Community-Patch/commit/8d922b42bef4b38c166173b89d9588a90a09b970).
- [September 1.0.0 update](https://github.com/Starfield-Community-Patch/Starfield-Community-Patch/commit/eaeb24a6909f4c3a4028433a57ff0a2786fde7cc).
- [June root tree API](https://api.github.com/repos/Starfield-Community-Patch/Starfield-Community-Patch/git/trees/8d922b42bef4b38c166173b89d9588a90a09b970).
- [Current snapshot root tree API](https://api.github.com/repos/Starfield-Community-Patch/Starfield-Community-Patch/git/trees/0ad97d3eb087dafb91afbc4bbb1588598212cc87).
- [May conversion limitation](https://github.com/Starfield-Community-Patch/Starfield-Community-Patch/commit/de993102e44a3015be2e0ab91030680a1f5a444b).
- [Release assets](https://github.com/Starfield-Community-Patch/Starfield-Community-Patch/releases).
- [Melee fix acceptance comment](https://github.com/Starfield-Community-Patch/Starfield-Community-Patch/pull/1045#issuecomment-2380857072).
