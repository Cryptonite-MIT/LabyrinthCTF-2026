# 24. acropolis

Author: hollo

Phase 3 | misc

Flag: `labyrinth{y0u_survived_th3_acr0palyps3}`

## Description

You’ve intercepted an email from Ariadne to Theseus. Icarus found an old phone in Daedalus’s workshop below the Acropolis, and something on it caught her attention. They might be the closest anyone has come to finding a way out of the Labyrinth.

## Solve

* The challenge provides you with an `eml` file with two attachments - `hexagon.txt` and a cropped screenshot from an old Gemini Pro 7 as mentioned in the email.

* The screenshot gives us a protected pastebin link, however the password seems to be cropped:

  <img width="1440" height="1532" alt="screenshot" src="https://github.com/user-attachments/assets/f2847ef6-6224-494b-bd3f-97c3733ecb95" />

***

 `Acropalypse` is a privacy vulnerability disclosed in early 2023 in which the cropped image looked fine but part of the original images data was still hidden inside the file. The cropped part of the screenshot can be recovered using https://acropalypse.app/, which gives us:

 <img width="1148" height="530" alt="image" src="https://github.com/user-attachments/assets/e406ac3c-ca58-4928-ace7-e3fd67991053" />

* Using this password we unlock the pastebin which says:

```
I‌​‌'‌​​v​‌​e​​​ ​​​s​​​t​​​o​​‌r​​​e‌‌‌d‌​‌ ​​‌t​​​h‌​​e​​​ ​​​a​​‌r​​‌c​‌​h​​​i​‌‌v​‌‌e​‌‌ ​‌​i‌‌‌n‌​​ ‌​​a​​​ ​‌​l‌​‌i​​‌b‌​‌r​​​a‌​​r​‌‌y‌​​ ‌‌​t‌​​h​‌​a​​​t‌‌​ ​​​h‌​​o‌​‌l‌‌‌d​​‌s​‌​ ​‌‌e​‌‌v​​‌e​​‌r‌‌​y‌​‌ ‌‌‌p​​​a​​‌g‌‌​e‌‌​ ‌​‌t‌‌​h​‌​a‌​​t‌​‌ ​​‌c​‌‌o‌​‌u‌‌​l‌‌‌d‌​​ ‌​​e‌​​v​​‌e​​​r​​​ ‌‌‌b​‌​e​‌​ ​‌​w‌‌​r‌​‌i​​​t​‌‌t‌‌​e‌​‌n​‌‌.​​‌ ‌​​H‌​‌i​​‌d‌​‌i​​​n‌‌​g​​​ ​‌​i​‌​n‌​​ ‌​​p​​​l​‌‌a​‌‌i​​‌n​​‌ ​‌‌s​‌​i‌​‌g​‌‌h‌​‌t​‌‌ ​‌​o​‌​f‌​‌f​​​e‌​​r​​‌s‌‌‌ ​‌‌p​​‌r​​​e​​‌t​​​t​‌​y‌‌​ ​‌‌g​‌‌o‌‌‌o‌‌‌d‌​‌ ‌‌‌protection, since nobody knows where to look.
```

* This text leads to Library of Babel and on going to https://libraryofbabel.info/browse.cgi we see that navigating the library required not only the hex provided earlier in `hexagon.txt`, but also Wall, Shelf, Volume and Page No.
* This information is hidden in the pastebin using zero width steg as hinted by `hidden in plain sight` which can be found using [stegzero](https://stegzero.com/) giving us everything we need to browse the library:

```
Wall: 2
Shelf: 3
Volume: 11
Page: 192

hexagon.txt: 2gzgxhjwimbuj1ppp4ccwaku4rhi1m9djy8600n1hmfwecl0ua5yo696o148yc5gx334ldmgbmlwvr2tw7krezkjtxerbhru5puf7thje221i70u1db670c61qrr4jgl64wlk1nvfkianh1q7ueledzs3tkhjbjrsqxrmbrq718qsh30li7d28amje347maeuqgtoy35vknmrx7vz8n6k0gcrv7b21mtb3tir4rf4olkp68gw3mc6ctiyvpau3341kw1vopmjp6eu62luaurwzuvgw0hwop27uwd6rg16w32qwv43cqmjbrjfxbttac6vbx17ca2csry5ncjnozv8rk9jk4mwwpsp66uxiumaezn825ntc34ez42cblpcognxy49zpj8jomd6o9i6pqvipt520yg5v1k6n325v0ud6cvcdtw68bp5rdlfhufjhkp1b453utw3uwvwwnaddsemzpcg4sdn51odqtzu94bqok2k5oeoogeyasnopq41gw2tc6i9imzr7zonjfpwmycsvr9331xiyai3tzcz4extaef9mdy19fuek2in0wcr63951mk6bikt3goxjaby6v4fqzbkssw87xjneuhj9r7rz6eaufoz0dw9ku6irbxcy3gt3nhqzu1r82uxbzpus8z6wuri8obrvly597rp2wb73gic42esio50a9h7yjg8r80fipsou1xqdgi8w5pzilp2vzbn0nitg50tcfulmrz5l3r0muayctamj59gbq7r9mxsk0qc4za8q9kstrrp5zus35soa9efss29dsfjiksatw11p7c1hzunjpo1go130qaq4cy8y6idvun75kzsbh1mk2yco1omsvjhong2u6ftbnic4zvj6m9iqyy3ofyn28rq51qb86h4mdv7trp3b7t5vhjtjmgnmshe6sgufeo5gbh1aulf63chg3s02l05a0z3lwcbtr06bk6xqz8p7vt9v4djwg6q4b4keron6cw9oozkzhn3u9b5comr2pmers2zonitpb6batv62et2iayp50wdiifut4eezr7md5lc7f736wvjymrdu92cjs4f8kzyud8547r5bzko6gjzihz1lqi2iel0wbkn0uup3ktezg8ci96san57g2nvr58sir97gq4o8guxq0nu0bm5xe840zot3n7q9ddyitnpu7mq8mp0mc2jz31fmw7f9braqp1pz00mz8cwqfjyc5n9rmhz09r49ryrftksbbfg78mv3yyugbv5rqgsg1a5mv8w9imqd8lunbec28welvyxhy64ob7xpi0gwwd6yqxtcrxcpka0cton72dsmuu1p4a8e6nzwx08jywk0zpvwusvi2jift9uiz3ynxz0dzfyxuhv1q51qtpxbe1i4dm45qbba61h53k4vx4au4ygy24vl85b6yjq0dui15if18olupbkgggiz9o9v9x7s89ku2rex2xvp7cyjs57o34f7tb6qet04q3yd6pyc1unn8p4ob5d4m0pw261sv5zphft07nv7thg7mx4am4au3bn2axvwv8qxqnz8vgdy5u0sac3x6aoxyced2b908lsxr6ocyckz6b9ho60a3sn2ie3g6ryubei56c2e8ee6evdlkwsqlbd8u2j70ywy365easet40w6zxx2qiswewrp6m367t8nrwk81nt1cjert3ufpyq6s14jibjvhevo0850j0lmv2reilxztw18ojyzlt3q0lj3mfzguy3jqdfr2cypajrdts6xjcrouynkyzm72r18asqjsyq76ncbtgufb1aypcx60sieggh2scylvnvtp02obo5mxqgbc3lrlhhvjjgf2sjjrz5rg7xedlym2ytj62x2cmi7o26dat3okqht6cnzt777ye412yr1391s31kn9v12sddifi67rlvfmzoxovkd45lqkgov0qnupgex6wd9x811hii0eppr0ke2ct858583jurnbpwassrhuril80rcu660cgf0dzlfdyrqgp7ey0hkr1snlrizp8ruukyrjy36dgcx3w1lp3ha36kc4cqlq9515jl83qkm31vtifo7jht052qv7n56i2ljmvza26k90fb3s418a2tgbqtfijnoxda6og1xwbei5afwxmv3uz9quyoiepiojfh4rgg3smz43pi2zyjdnigz2pru3n6hcchcww5ro456lkirohed9qgnykagjljdbdmd6xbozgids5vpf1krfi153gw2fwz7c5txoc636mwpvun0oamnagahscw8jctq5o2l26iadxb9ngasqw45ywy7sutg0yl762t2hzbif7hu2kz6xvily8d1tsnpthat9lwpd6hok0r007qxnbid0fel2wrn6hucsd08kro2qxktc1mtv6l7qjbk1mmhtlwnrbfe1bdf7uhg2j8p8ujkdz0qk0gzy6ogp9o17cl5v25guffvvuyphynhqplg034bxi6w957fafhvfqiv0h22cdmkzne4xetvvr5byk3miq5feu9x88rwkexzaikigixl101n5ytjbu88x2axuifm73fkgn652u6qvsfuj9pueep82opl24ubhgt2c0piapdixi60s11l2mszpxffvcsro0hi4mscuntxp2n75wmxcxh65jnijun5ibjjlqaq26uzedyuxy071z9zt2rpuhm7923ny1yd0k3d7898uesh8d316ovfb2v744nlzg9omkejybjq95y1s4z7kxua6ag66vp3a5vp1tvjbhc7ofj93l67t8fvbigcpwn7mds84rd5wggmayo2n6275dind8ys3y5k8f8rfz4yphid8tx81lebfx2sbvofxw4ztqc15dwaaqa7pmk50fqyhyqfrldq56v9vkif9g522ou4rmm1cc5pj6zve20vk25e5nlneox576ksrv9o6rg9c3noywxx7twq6zvus6tu2uqn5664q5olbla0qhh9cqf6oj5nirmlcn83xgxftohqhq7xudikl78d9j2kfhloz13fh335we38c7r59ev0mmrv2cip4n7bre3pc1z8ygx5aryylm07txu9t9axcgodleejbfpjbamjemrofdpxnl9ax8kvh6xpm7rp5fxyo3gjqcv85g2d9hnttt44vgvomvxpiju189ttle5yzt2qwzk9ybs6xgz1p8nqwpbr99qljpqvaacqew8as95rmzzrm2lp2ekoi5bdnxyj2eaf5pj157i42ke16zmt
```

* Using the provided details, we find a page with text that can be identified to be PGP `(pretty good privacy)` wordlist cipher using using https://www.dcode.fr/cipher-identifier and on deciphering we get our flag.

