# 21. Tablet of Knossos

**Author**: fudgesupreme

**Category**: forensics

**Difficulty**: Medium

## Description

You managed to find the secret ingredient but the key it contains failed to unlock the next room. On looking around more deeply, you see that there remain signs of something that used to be there. Its was shattered and its fragments were scattered across the dark corridors of the labyrinth. However, nothing in the labyrinth is truly lost. Some objects are merely unreachable. Uncover what lies beyond the visible branches to piece together the thread and escape.

## Solve
- You are given a zip which contains `.git` folder and a `secret.md` file which just states that the flag has been hidden inside this folder and has been divided into 16 parts.
- So We need to find the parts, as this in inititalized with git
- Flag is divided into 16 parts combine all and wrap in `labyrinth{}` wrapper to get the complete flag and submit.
- Now as the folder is initialized in `git`, i checked the `git log` using the following command :
```
  commit 608a7a483206f909ca3f713c9b4f5852edcc8614 (HEAD -> master)
Author: daedalus <daedalus@knossos.gr>
Date:   Tue Mar 3 10:00:00 2026 +0000

    seal the northern gate

commit b4047973519d06f962fb54daa5366713a0aacc6d
Author: daedalus <daedalus@knossos.gr>
Date:   Mon Mar 2 10:00:00 2026 +0000

    add the hall of mirrors

commit ab24f62c0eee6865a6e6e4ccf55a20809a1abe99
Author: daedalus <daedalus@knossos.gr>
Date:   Sun Mar 1 10:00:00 2026 +0000

    chart the first corridor
(END)
```
- found nothing useful here so i checked out `git fsck` which basically checks the repo and can list objectsthat point to nothing and basically unreachable
```
❯ git fsck --unreachable --no-reflogs
Checking ref database: 100% (1/1), done.
Checking object directories: 100% (256/256), done.
Checking objects: 100% (25/25), done.
unreachable commit cdb855df2f8f3b39473051120ca48e58e5fd1583
unreachable commit 8e0e59ec9639aa0b57e1a1b9d2d5c10cad7e86e8
unreachable commit 91f26cf458c65ee42563af9f96e58bd5effbd048
unreachable commit 937f93c6601f545e4db315c4398e1fe05713105d
unreachable commit 59fc0db2c635bdc95c97d122b865a2b336fa7442
unreachable commit db4acaa12699006a6bc5b7f894971b120799c2a5
unreachable commit 20cedd8420c987469708da94209b3801336c1b77
unreachable commit a8184dfdb5f5dd2ec22382c87c101fdadd9de86f
unreachable commit 6ad8fe916e4edeec76358bc0aec1653eab6a3b62
unreachable commit 2c5f072d82bffc852bdbeadca334b9e1119b666d
unreachable commit b0569a15ca368820738213e9f868f88fc51a372e
unreachable commit b153cb537d52b93aa219f1e0f7a6ad89e87fcc37
unreachable commit f2c28ef15d40ecb044c445028da60f676021bd43
unreachable commit 3781b0fbc7ae670699138322320c77c9790febc2
unreachable commit fdb5e7c02da5192783bcfddd31ae0270990ee787
unreachable commit fda7014d60f9e5b9d8b12e7a670a04a7f8f16b37
Verifying commits in commit graph: 100% (3/3), done.
```
- this showed 16 commits which were unreachable, on catting 1 of the commits i found this :
```
❯ git cat-file -p cdb855df2f8f3b39473051120ca48e58e5fd1583
tree 4b825dc642cb6eb9a060e54bf8d69288fbee4904
author daedalus <daedalus@knossos.gr> 1773154800 +0000
committer daedalus <daedalus@knossos.gr> 1773154800 +0000

corridor 15: 2e4e
```
- so these are the 16 parts the flag was divided into, now initally i thought combining themm using corridor no was the right asnwer but it wasn't and the commit times were forged aswell\
- Inside the `.git/objects/pack` folder has a `.mtimes` file, which records when git actually wrote each hidden object.
- I paired those times with the object IDs that are present in the `.idx` file
- to do that follow the following steps :
  - get IDX file which has the same id as the .mtimes file
  - then dump out the oids from IDX file, can do it manually or auto from the following command :
  ```bash
  git show-index < $IDX_FILE | awk '{print $2}' > oids.txt
  ```
  - There are 16 oids
  - Now get the timestamps from the mtimes file, for that u need to strip out the initial metadata and out exactly 4 bytes which is the timestamp per line.
  ```bash
  tail -c +13 .git/objects/pack/*.mtimes | xxd -p -c 4 | head -n 16 > mtimes.txt
  ```
  - Now sort them and get the oids in order and then read them
  ```
  paste mtimes.txt oids.txt | sort
  ```
  - Read using : 
  ```
  git log -1 --format=%s <oid>
  ```
- the final result would look like this:
```bash
❯ ls
pack-4126661210b8be93d19f11d1edb98e90380c94bc.idx     pack-4126661210b8be93d19f11d1edb98e90380c94bc.rev   pack-7a4eccc1d66f68e833f0e569128d655babbbce05.rev
pack-4126661210b8be93d19f11d1edb98e90380c94bc.mtimes  pack-7a4eccc1d66f68e833f0e569128d655babbbce05.idx
pack-4126661210b8be93d19f11d1edb98e90380c94bc.pack    pack-7a4eccc1d66f68e833f0e569128d655babbbce05.pack

❯ git show-index < pack-4126661210b8be93d19f11d1edb98e90380c94bc.idx | awk '{print $2}' > oids.txt
❯ cat oids.txt
20cedd8420c987469708da94209b3801336c1b77
2c5f072d82bffc852bdbeadca334b9e1119b666d
3781b0fbc7ae670699138322320c77c9790febc2
59fc0db2c635bdc95c97d122b865a2b336fa7442
6ad8fe916e4edeec76358bc0aec1653eab6a3b62
8e0e59ec9639aa0b57e1a1b9d2d5c10cad7e86e8
91f26cf458c65ee42563af9f96e58bd5effbd048
937f93c6601f545e4db315c4398e1fe05713105d
a8184dfdb5f5dd2ec22382c87c101fdadd9de86f
b0569a15ca368820738213e9f868f88fc51a372e
b153cb537d52b93aa219f1e0f7a6ad89e87fcc37
cdb855df2f8f3b39473051120ca48e58e5fd1583
db4acaa12699006a6bc5b7f894971b120799c2a5
f2c28ef15d40ecb044c445028da60f676021bd43
fda7014d60f9e5b9d8b12e7a670a04a7f8f16b37
fdb5e7c02da5192783bcfddd31ae0270990ee787

❯ tail -c +13 pack-4126661210b8be93d19f11d1edb98e90380c94bc.mtimes | xxd -p -c 4 | head -n 16 > mtimes.txt

❯ cat mtimes.txt
69b4c8dc
69b4c7ce
69b4c3f0
69b4c60c
69b4c44a
69b4c4a4
69b4c6c0
69b4c828
69b4c666
69b4c558
69b4c936
69b4c5b2
69b4c71a
69b4c774
69b4c882
69b4c4fe

❯ paste mtimes.txt oids.txt | sort
69b4c3f0        3781b0fbc7ae670699138322320c77c9790febc2
69b4c44a        6ad8fe916e4edeec76358bc0aec1653eab6a3b62
69b4c4a4        8e0e59ec9639aa0b57e1a1b9d2d5c10cad7e86e8
69b4c4fe        fdb5e7c02da5192783bcfddd31ae0270990ee787
69b4c558        b0569a15ca368820738213e9f868f88fc51a372e
69b4c5b2        cdb855df2f8f3b39473051120ca48e58e5fd1583
69b4c60c        59fc0db2c635bdc95c97d122b865a2b336fa7442
69b4c666        a8184dfdb5f5dd2ec22382c87c101fdadd9de86f
69b4c6c0        91f26cf458c65ee42563af9f96e58bd5effbd048
69b4c71a        db4acaa12699006a6bc5b7f894971b120799c2a5
69b4c774        f2c28ef15d40ecb044c445028da60f676021bd43
69b4c7ce        2c5f072d82bffc852bdbeadca334b9e1119b666d
69b4c828        937f93c6601f545e4db315c4398e1fe05713105d
69b4c882        fda7014d60f9e5b9d8b12e7a670a04a7f8f16b37
69b4c8dc        20cedd8420c987469708da94209b3801336c1b77
69b4c936        b153cb537d52b93aa219f1e0f7a6ad89e87fcc37

❯ git cat-file -p 3781b0fbc7ae670699138322320c77c9790febc2
tree 4b825dc642cb6eb9a060e54bf8d69288fbee4904
author daedalus <daedalus@knossos.gr> 1773126000 +0000
committer daedalus <daedalus@knossos.gr> 1773126000 +0000
```
- Now We had to manually cat each file and complete the whole flag by appending it in the following order to get the flag.

### Flag
```
labyrinth{8b2fc193490273320d272e4e7631b47a1cf01f5e673eb239995e1f71ffef9437}
```
