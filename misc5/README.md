# Bonus 1 - Promposal
---
### step 1: what to do with an email
take his email address walter.goose.wxm@gmail.com. seeing that it says its an event that they are meeting up and i guess with a gmail account one they that could be tried is using ghunt to find their public google calendar.
using ghunt, you can see this!
![image](https://github.com/TheRealGecko/wxmctf-2024-admin/assets/80985676/73722791-88ae-428b-98ff-a21008cbacc8)

### step 2: calendar!
downloading the .ics file you get some information, but to be sure here's what you get when u import the url into google calendar
![image](https://github.com/TheRealGecko/wxmctf-2024-admin/assets/80985676/956cdc8c-6bbd-453a-9cb1-6af0d13ecff0)

from this you can get
- vera.aloe.wxm@gmail.com
- may 1, 8-9pm est
- massey hall
- 8/18
- cover on a singing app (with a guy with a black and white pfp and 🤎)

the most obvious thing you can do is google whats going on at massey hall at may 1, 8-9pm (especially if it says that vera likes music and singing), which is a laufey concert!

### step 3: smule
(a) using socmint tools, you can find that vera has a smule account
 - you would also be able to find that she has only one cover under her account
 - or u guessed smule and found account by adding from contact

(b) if you didnt do that, you can maybe infer from 'cover on a singing app' that it's smule (most popular one)
 - taking laufey and 8/18 (promise is the 8th song from her setlist that concert - i think this was a bit hard to get)
  - if you didnt get the promise part you can maybe go through laufeys most popular songs and find a guy with a black and white pfp as the dueter
   - smule not vip version uses a system where you have to duet someone
   - the specific cover has the 🤎 in the post

after finding the cover, you immediately hear some robotic beeping - not a voice lol

pretty obvious that it is morse code (if i made it cancer i couldve distorted the beeps to be very nice sounding)

unmorsing it and reading the pfp telling to read the bio says to lowercase and capitalize certain characters you get 2an1fDbYGA5fGnKVMHlGGd 

### step 4: spotify
if you socminted walter, you can see he has spotify (vera does too but its kinda useless for her) but you wouldnt be able to see anything on his profile

but you can maybe guess from 'she likes music' or the way the series of characters is formed (and me going out of the way to uppercase some characters that makes it more obvious that its case sensitive and maybe a URL) can maybe guess its a spotify playlist link

doing https://open.spotify.com/playlist/2an1fDbYGA5fGnKVMHlGGd 

the series of songs have a very nice message for vera (uwu) with the last bit telling her to [wear, your favorite dress, please] and in the description theres the 6 character hex 

### step 5: flag
combining everything together you get:
`wxmctf{M5B1T7_promise_favorite_dress_2b3e98}`

### tools:
https://epieos.com/ (ty replay on discord)

