import sqlite3
import torch
from transformers import pipeline

device = 0 if torch.cuda.is_available() else "cpu"
from audio_processing.utils import preprocessing_functions as pf

conn = sqlite3.connect(r'D:\AmbiLab_data\quant_neg_data.db')
cursor = conn.cursor()


def localize_segment(utterance) -> int:
    import math
    """
    Finds if the utterance is in the first half of the audio by searching through
    the document
    """
    sentences =[
        "NEAL CONAN, host: This is TALK OF THE NATION. I'm Neal Conan in Washington. Last week, a coroner's report provided the details of a verdict that everyone already knew. Singer Amy Winehouse drank herself to death. Her blood alcohol content was five times the legal limit when she was found in her London home in July.",
        'Her mother told reporters she long felt it was only a matter of time, a phrase that may resonate with those of us whose adult friends or loved ones face serious problems with drugs and alcohol. What can you do to help? Can help become counterproductive? Is there a time to cut off support?',
        "If this is your story, give us a call. Our phone number is 800-989-8255. Email us, talk@npr.org. You can also join the conversation on our website. That's at npr.org. Click on TALK OF THE NATION. Later in the program, Jordan Tama argues in defense of the backroom deal as the clock counts down on the congressional supercommittee.",
        'Bur first, David Sheff, who told his story in the book "Beautiful Boy: A Father\'s Journey Through His Son\'s Addiction." And he joins us from member station KQED in San Francisco. Nice to have you with us today.',
        'DAVID SHEFF: Thank you, Neal.',
        'CONAN: And have - did you ever worry about your son Nick, that it was just a matter of time?',
        "SHEFF: Oh God, yeah, for years. It was a matter of time for years. So you know, when you hear about something like Amy Winehouse, everyone else - I mean, there's a lot of celebrity watchers who sort of treat it as entertainment but, you know, when anybody who's been through it hears it, it just breaks our heart.",
        'CONAN: And how is your son doing?',
        "SHEFF: You know, he's doing great. He's been sober for - I guess it's been about four years. He got married this summer. I mean, all these things that were unthinkable when he was, you know, in his early 20s, and we didn't know if he was going to survive.",
        'CONAN: You wrote a book. He wrote a book, too, about his meth habit.',
        'SHEFF: Yeah, he did. You know, he was - growing up, he was a really good writer and at one point, you know, he was asked, you know, to tell his story, and he did, and it was a pretty powerful book. It was - you know, for a father to read about the horrible, horrible experiences my son went through, is - you know, it was just unbearable.',
        "But, you know, the book actually has - you know, from what I've heard, you know, it's touched a lot of people, especially teenagers, and he's been speaking at high schools. And I think it's been pretty remarkable that, you know, kids will write or call and say that - or parents will tell me that, you know, after a conversation with Nick, they've - you know, their child has told them that they've been in trouble, or a principal has said that, and they've ended up going into treatment.",
        'CONAN: Going into treatment - Nick was in and out of rehab.',
        'SHEFF: He was in and out of rehab - oh God, what is it? Seven or eight times; inpatient programs, outpatient programs. And then in addition to that, you know, sober living houses, halfway houses. You know, it was about five, six, maybe even seven years of hell.',
        "CONAN: Hell - I don't think that's too strong a word.",
        "SHEFF: It's not. You know, any - but it's - I think it's one of our biggest fears. You know, I mean, any parent, you know, we just worry about our kids so much, and there's so much to worry about. And I think, you know, drugs is sort of up there and probably number one - if not, you know, number one or number two - because, you know, it's - you know, it's so pervasive.",
        "You know, there's so many mixed messages. It's so confusing for kids. It's really confusing for adults. We just, you know, don't know how to navigate this whole thing.",
        "CONAN: And it gets so much harder. It's your child, but once he's 18, there's not much you can do.",
        'SHEFF: Yeah, by the time I sort of figured out what was going on; that, you know, how serious this problem was and how, you know, Nick really, really, you know, could have easily died; he had turned 18. And you know, before that, you know, a parent has more ability to make choices for their child - I mean, to get him into rehab.',
        "And after that, though, you know, Nick had to walk in of his own volition. He had to sign the papers and, you know, anybody who's high or anybody who's using drugs and, you know, anybody who's addicted, you know, that's not what they want to do. I mean, they have every reason to avoid that at all cost.",
        "CONAN: And then there is the question of, he's your son. Do you support him? Obviously, emotionally yes, but financially?",
        "SHEFF: Well, that - you know, that was hard for me, and I think it's hard for anybody because, you know, it's sort of - I don't know. There's sort of these mixed messages and certainly, there's conflicting emotions. I mean, you know, it's our kid. You know, Nick was out there on the streets. He was in - you know, he was beaten up. He ended up, you know - they almost had to cut his arm off in a hospital because his arm was infected.",
        "He was in emergency rooms. I got a call once from a doctor who told me, you know, Mr. Sheff, you'd better get down here; we don't know if he's going to make it. So, you know, when I would hear from him, you know, I just wanted to do anything to assure that at least for that night, he was OK.",
        'And so for a while, I did give him money, and I did let him come home and sleep it off. And he would promise me that, you know, everything was - he learned his lesson, or whatever. And then the next morning, by the time, you know, the next morning came, he ',
        'was gone again.',
        "So eventually, you know, that's where I got. I got to the point that, you know, I realized that everything I was doing was not helping him. So I would never, ever - you know, people in this, you know, world of rehab and addiction, you know, they tell you you have to let go and let a person hit bottom.",
        "I mean, I never got there. I mean, I never, ever could let go of my son. But I did realize that what I was doing wasn't helping, and so I think what made a big difference - certainly for me, and I know, you know, he talks about it, that it made a difference for him - was when he called up one time. It was one of the worst ever. You know, he was near death again. And he said, you know, I want to come home. You know, will you come get me? And I said: I'll come get you, and I'll take you into a treatment place, and I'll set it all up. And he said: No, you know, I've done that before. It doesn't work for me. I've been there.",
        "And I said: You know, Nick, I love you so much. Anytime you're ready to get help, call me. And I hung up the phone, and it was the hardest thing I'd ever done in my life. I lost it. I was just a wreck because I knew that I - you know, the next phone call I would get, you know, could be, you know, the worst. I mean, he, you know, something irreparable or damage or death.",
        "But nothing else had worked. And you know, what happened was, I think it kind of was part of what woke him up. And he realized, you know, he'd better do something, and he had to do it on his own. And finally he did call and he said, you know, he needed help.",
        'CONAN: Let\'s get a caller in on the conversation. We\'re talking with David Sheff, author and journalist, the author of "Beautiful Boy: A Father\'s Journey Through His Son\'s Addiction." And we\'re talking about what do you do when you\'re worried that it\'s only a matter of time; 800-989-8255. Email talk@npr.org. Bianca\'s on the line, calling from Piedmont, California.',
        "BIANCA: I thank you so much for your book. I think it's going to be a really important story because listening to you makes me want to cry. It so mirrors my own experience with my little brother. And he went in and out of rehab in his young 20s and finally - I'll never forget it - he was living with me and my kids, and I was going through a divorce, and I had to kick him out.",
        "And he got himself into a rock-bottom situation, and he also asked, you know - said that he wanted some money. And I used to always give it to him. And I didn't really understand that I was enabling him.",
        "And in the end, he is clean and sober four years out, and he is a magnificent and amazing human being. And I'm just so glad that we didn't give up on him. And what made the difference in our family was that we did an intervention, and he just - he came to understand that he needed to stop because it was not just destroying himself, but it was destructive to everyone else who loved him as well.",
        "And a really important point that I wanted to make is that - what I learned through a friend who's a therapist is that if you are somebody who is using drugs and alcohol, and you get help and go through rehab, if you return to the place where you were living before, and to the families and the friends and your old ways, there's a 90 percent recidivism rate for those people.",
        "They have to be physically removed from the things that were tempting them, so to speak. And so my brother actually now lives in Florida, and he runs AA meetings, and he's a model citizen and just an amazing person. So thank you very much for your work, and I hope that it will help save other lives.",
        "CONAN: And we're glad things worked out, Bianca, and with your little brother.",
        'BIANCA: Yes, me too. Thanks. OK, bye-bye.',
        "CONAN: They don't always. Here's an email we have from J.D. in Minneapolis. Went through an intervention with my college boyfriend, and my consequence for his decision to decline treatment was that I would not see him again.",
        'Years later, his parents called to inform me that he drank himself to death. A very painful decision at the time, but I feel I did the right thing. And David Sheff, to make that decision, you have to be - well, you talked about it a moment ago. You have to be ready to deal with the consequences.',
        "SHEFF: Yeah, and the truth is, you know, if it's someone you love, you never are. You just, it's - you know, it's like this line, this wavering line. You know, a lot of things kind of wake you up, and it happens slowly, and then there'd be a regression, and I would be so freaked out that, you know, anything to make sure he was OK.",
        "But that whole idea of enabling, I mean, I was at, you know, a family group at one of these rehabs, and this woman was talking about, you know, weeping about, you know, her son and helping her son. And she was saying that, you know, that I have to give him money. I have to - you know, I don't want him to starve. He needs to eat. He needs a place to stay. So I give him money for a hotel, you know, this sort of...",
        "And the counselor said, you know, he's not as helpless as you think because if he wants to go over the - you know, get from San Francisco to Oakland to go to his dealer and, you know, get money for drugs, he's able to do it. And, you know, raised the question: Are you helping him? Are you helping him get better, recognize, you know, that - suffer the consequences of what's happening in his life and what the choices he's making - or not, you know, allowing him to keep using?",
        "CONAN: Joining us now from a studio at the Mayo Clinic is Dr. Terry Schneekloth, where he's director of the addiction services and assistant professor of psychiatry. And it's good to have you with us today.",
        'DR. TERRY SCHNEEKLOTH: Thank you very much.',
        "CONAN: And this question of enabling, what do you tell parents, friends when they're worried that they're not helping anymore?",
        'SCHNEEKLOTH: You know, David expressed this so well, the battle he continuously had of what was going to be helping his son the most, and not wanting to enable him but not being able to let go, either. And it took such bravery to do what he did that night that Nick called.',
        "And was there. He was offering help. But Nick didn't accept it at that time. And as he mentioned, Nick called back, and Nick went on to get help. And it often takes that kind of holding the line for family members. And that's incredibly difficult to do and often, it needs to be sorted out as you go.",
        "And so this is difficult for families. They struggle with it. But I'm very impressed with David's story of how he listened along the way, he participated in the family work. He tried to sort out what would be best for him, for the family, to help Nick. And it's a wonderful, very helpful story of how his son recovered.",
        'And the majority of people with addictions do recover, and they do better when they have family members that are trying to help them with the process and sort it out and seek help, like David did.',
        "CONAN: We're talking about difficult decisions when someone you love seems to be spiraling out of control with drugs or alcohol, or both. What do you do when you fear it's just a matter of time?",
        'If this is your story, give us a call, 800-989-8255. Email us, talk@npr.org. We\'ll have more with our guests, David Sheff, he\'s the author of "Beautiful Boy: A Father\'s Journey Through His Son\'s Addiction"; and also with us,  Dr. Terry Schneekloth, assistant professor of psychiatry and director of addiction services at the Mayo Clinic. Stay with us. I\'m Neal Conan. It\'s the TALK OF THE NATION from NPR News.',
        '(SOUNDBITE OF MUSIC)',
        "CONAN: This is TALK OF THE NATION from NPR News. I'm Neal Conan. Nearly 40,000 Americans die every year from drug abuse; alcohol-induced deaths number more than 20,000, excluding accidents and murders. That might be your neighbor, your friend, your son or daughter caught in a spiral of substance abuse.",
        "We're talking today about what you can do when you fear the worst, that it's only a matter of time. If this is your story, give us a call, 800-989-8255. Email talk@npr.org. You can also join the conversation at our website. That's at npr.org. Click on TALK OF THE NATION.",
        'Our guests, Dr. Terry Schneekloth, director of addition services at the Mayo Clinic, where he\'s also an assistant professor of psychiatry. David Sheff is with us, too. He\'s the author of "Beautiful Boy: A Father\'s Journey Through His Son\'s Addiction."',
        "And let's see if we can get another caller on the line. And let's go to - this is Nicolas(ph), Nicolas with us from Duluth.",
        'NICOLAS: Hello.', "CONAN: Hi, Nicolas, you're on the air.",
        "NICOLAS: Hi, thanks for taking my call. I was just going to say that I'm on the opposite side of that. My father was actually addicted to alcohol, and my family had to take him in and out rehab for years, years and years and years. And he passed away from drinking because he was alcoholic and whatnot. And I just wanted to make a comment to make people aware that people who suffer with addiction, that it's a disease.",
        "Like, it's just like any other disease on the planet, any other disease that kills people, and from that, depression becomes their crutch. And they will use that over and over. They can only accept help if they want it, and people just need to know that you can only give out so much love until it ends up being a lost cause no matter how bad it hurts.",
        "It still just doesn't – it won't always pan out the way it needs to be able to pan out, but to never give up.",
        "CONAN: I'm sorry at your loss, Nicolas, and thank you very much for the phone call. And there's a couple of points that Nicolas raised that I wanted to address. And one of them is that pattern, in and out, in and out. David Scheff, you mentioned this a little while before. Obviously things have worked out better with your son Nick, but that frustration, another program, another sober living house.",
        "SHEFF: Yeah, it's - you know, the first time I sent him to a program, it was a 28-day program, and even though that was hard, I thought: Oh, thanks God, you know, I'll pick him up in 28 days, and he'll be fine, and we'll move on from this.",
        "But, you know, Nicolas ,who just called, was exactly right. I mean, I'd learned the hard way and over a long period of time that this is a disease. It's, you know - addicts' brains are different than the rest of ours, and, you know, just like, you know, if a person you love has another disease, you know, sometimes it takes a while, you know, and if you get help, and sometimes it comes back, and then you try again, and then sometimes it comes back again.",
        "And, you know, and it's, you know, it's a progressive disease, and it's a chronic illness is what they say. And, you know, that helped me a lot in terms of even this decision about how to help and not help because once I realized that he was ill, I was able to take it less personally. It wasn't necessarily my fault, although I don't know if I ever completely believed that.",
        'And then, you know, I was able to be more compassionate. You know, instead of how could you do this to us, it was more like oh my God, my poor son is ill and needs help.',
        'CONAN: Ill, and I wanted to bring Dr. Schneekloth in there. Yes, a disease. Does it not also involve, though, some element of character? Many people wonder if willpower can help people.',
        "SCHNEEKLOTH: You know, well, ultimately there needs to be the choice that one wants to stop. But that's often when the pressure increases to a point that there seem no alternatives. The American Medical Association has identified alcoholism as a disease going back to the mid-1950s, and as Nicolas pointed out and David that it's so important for families to come to see this. Otherwise, they can feel like it's their fault, shameful, guilty.",
        "As they see it as a disease that's really taken over their loved one's life, it allows them to step back and to address how they're going to cope with it and to see that the disease is going to take its course, that there are ways in which they can intervene, but ultimately the decision needs to be made by the one with the addiction: Are they going to stop?",
        'Now, some people can stop on their own. As a matter of fact, the majority of alcoholics stop, never receive addiction treatment, go on to do well. There are different types, though, and some have more severe forms of addiction and need multiple treatments.',
        "I might add that the disease of addiction is really very comparable to similar chronic illnesses like diabetes, hypertension and asthma where there are repeated exacerbations of the illness, that it comes back. And in the same way with addiction, relapse is often a part of it. Now, families can feel like that's somehow a failure, but often one treatment builds on another and eventually leads, like Nicolas' story, to ongoing recovery.",
        "CONAN: Let's go next to Ken(ph), Ken with us from Tucson. Ken, are you there? I guess Ken has left us. Let's try instead to go to Joe(ph), and Joe's with us from Charlotte.",
        'JOE: Yeah, I got out of college in 1977 and went straight into the field of addiction treatment, everything from counselor all the way up to clinic director. So - and I spent 20 years doing that. I knew the ropes real well. My oldest son, after the Army, showed signs of addiction. We began working with him, trying our best to pull him out of it.',
        'He spiraled deeper and deeper into it. Eventually we realized that he was dual-diagnosed. He was schizophrenic, and he was medicating himself with whatever he could get his hands on.',
        'Eventually we had to tough-love him. He ended up in the county jail for a year. He ended up in Broughton. We tough-loved him through the whole thing. But during this process, my younger son, who was 21, he began to experiment also, and he began to hang out with the kids from his high school who were experimenting.',
        "When he was 21 years old, they went out getting high and drinking, and the girl driving the car wrecked the car. My son was killed, and everyone else in the car lived. So we lost one son. And the oldest son is now again sober for, I don't know, two or three years. He's on medication for schizophrenia, and he goes to AA, and he's been clean and sober.",
        "And in my work in addiction, what I realized is that something that AA tells you is very, very true, and that is there are people who are constitutionally incapable of that form of recovery, and there's just something about them that almost can't be helped.",
        'But in our case, with tough love and with standing firm and with understanding addiction the way I did, we were able to save one son.',
        "CONAN: And congratulations on that, and we're so sorry for your loss. But given your profession, David Scheff mentioned, and so did Dr. Schneekloth, the guilt that people feel. It must have been how could I miss this, how could I - did you feel like you let your sons down?",
        "JOE: Well, you go through such a range, a spectrum of emotions when you lose a child. But the one thing that I think - well, not the one thing but one of the major things that I really learned through the whole experience of both the 20 years of addiction treatment and having lost a child is - and I know this sounds a grave thing to say, but I really believe it's true - no matter what you do, in the end result, you really can't protect them.",
        "You can just give them the very best you can give them and hope that it's the thing that makes the difference. In our case, one, it made the difference and the other we lost before we were able to really grasp him and help him out of it.",
        'CONAN: Joe, thank you for sharing the story, and appreciate it.', 'JOE: Sure.',
        "CONAN: And here's an email that's on the same point from Kevin(ph): As a recovering alcoholic and addict, I would argue that any action which helps the addict to avoid taking responsibility for his own actions is in fact not support at all. The one most important thing my parents did right was to give me unconditional love and maintain the bridges connecting us.",
        "And Dr. Schneekloth, we hear different expressions: tough love, no you've got to make sure that they do have a place to stay and, you know, unconditional - does it vary case to case?",
        "SCHNEEKLOTH: I think it does. Now, the unconditional love being available to help them into treatment, into - to receive help whenever they're ready for that, I believe that that needs to be there in support of families that can offer that. But starting out from that point, where you start in, where you help out, when you provide shelter, very tough for families. And it needs to be individualized.",
        "I'd like to go back to what Joe from Charlotte said, too, about his family members that had both addiction and an emotional problem because so many people with addictions have that. And that may impact how a family member acts and how they support them. And it's so critical for treatment to address both problems at the same time because addressing only the addiction when there is an emotional problem going on as well is only going to get at part of the solution and may be a contributor to someone going back to using.",
        "SHEFF: I'll just say quickly that that was Nick's, my son's situation, too. And it took a long time because, you know, when someone's using drugs, it's hard to see what else is going on. But Nick finally was diagnosed with bipolar disorder, and he's on medication for that. And he would say that that's one of the biggest components of, you know, this recovery that he is now, you know, able to pull off.",
        "CONAN: Here's an email from Margaret in Rochester Hills, Michigan: When I finally went to Al-Anon, it saved my life. There are two addictions involved: the alcoholics to drink and the enablers' addiction to trying to help. I had to break my addiction first. In my case, my alcoholic never recovered, like Amy Winehouse, but I did.",
        'David Sheff, I know you have experience with Al-Anon.',
        "SHEFF: I did, and I, you know, really resisted it for a long time. I thought I was, you know - I didn't know about it, I guess. But I thought there was going to be sort of a bunch of people in a room whining and drinking bad coffee and whatever. But, you know, I was just so desperate at one point that I would have done anything, and I did go. And as soon as I walked into one of those rooms, I realized, you know, I needed to be there. And these were people that were like me. It was - you know, they were like me because they understood exactly what I was going through because they were going through it too, and it really helped a lot.",
        "CONAN: Let's see if we go next to Cathy, Cathy with us from Kansas City.",
        "CATHY: Hi. I just wanted to ask Dr. Schneekloth - I'm sorry - about the advisability of forcing a person into treatment if you're just hoping for a break in the cycle. My adult son is - does have emotional problems and refuses counseling, and I believe he is just really spiraling down. In fact, I know he has a death wish. So I don't know that this would be helpful.",
        "SCHNEEKLOTH: Well, what pressures you have available I would encourage you to use, certainly to express your concerns, to encourage him to get help as he's an adult. If he's unwilling to do that, that is as far as you can go. But you know, often a simple intervention of talking with him, going to the family physician with him and the three of you discussing it together may be a step to get him help. And certainly in a good treatment program you don't know what can happen. Often when someone is just in a cloud of their addiction, they're not able to see what's going on.",
        "Now, there are also, you know, interventions that can occur with family members in contacting county social services if you think that there's an imminent danger that someone has, and that's really the only time you're able to force an adult into treatment that they don't want against their will.",
        'CATHY: OK. Thank you.', 'CONAN: Cathy, good luck.', 'CATHY: Thank you.',
        "CONAN: And I wanted to get back to you, David Sheff. And there is sometimes almost - your son was addicted to meth, which is incredibly destructive, incredibly addictive and causes all kinds of problems in addition to the addiction. It must be especially frustrating. Not to say that alcohol is easy or heroin is easy or anything. It's not. They're all addictions, and to some degree they're all the same, but meth causes so many other problems.",
        "SHEFF: Yeah, it does. And when Nic - Nic said that, you know, he was using other drugs, but when he tried meth, you know, it was it for him. And he went - that's when the spiral down - it just completely took over his life. And, of course, you know, people - I don't think most people just use one drug. And so he ended up using every single drug you can think of. He was shooting heroin, he was using crack and he was taking every pill he could get.",
        "But it did, you know, pose extra challenges when he did get into treatment because, you know, meth makes you crazy, and he was pretty crazy. And, you know, if it were not for the fact that, you know, he got - he was in the care, finally, of good doctors, and we were really lucky. And he, you know, we were just so lucky because, as so many people have said today, you know, a lot of people don't make it.",
        'CONAN: David Sheff\'s book, "Beautiful Boy: A Father\'s Journey Through His Son\'s Addiction." Also with us Dr. Terry Schneekloth, assistant professor of psychiatry and director of addiction services at the Mayo Clinic. You\'re listening to TALK OF THE NATION from NPR News.',
        "And back to an email on a subject that we've mentioned before, this one from Brenda: Much of addiction is masking or coping for mental illness and/or brain damage. Tough love and enabling won't really change the underlying problem. How do treatment programs identify this issue?",
        'Dr. Schneekloth, can you help us out?',
        "SCHNEEKLOTH: It's often very complex, and I believe it's the reason that it's important to get family members to competent care providers. None of us would take our family members to a general physician who's practicing 1960s-era medicine. We shouldn't be doing that with family members, to take them into addiction treatments that really haven't kept up on the advances in the brain science.",
        'So many incredible things have changed in our understanding of the neurochemistry of addiction, what causes it, the psychiatric diagnoses which may occur at the same time, or the symptoms that look like a psychiatric diagnosis that someone may have from their substance use. And that needs to be teased out in a safe setting by highly qualified professionals.',
        "I know in our own practice here at the Mayo Clinic over the past 50 years, we've had to continuously change those treatments based upon the advances in the science. For instance, there are now medications available to help people with craving for alcohol, which are seldom used in the United States. Many people with alcoholism don't have that as part of their treatment. So it's important to have a treatment program that's going to look at everything, look at the emotional problems, the general medical health, as well as providing addiction treatment that's state-of-the-art.",
        "CONAN: Let's get one more caller in. Leslie is on the line, Leslie with us from Kansas City.",
        "LESLIE: Yes. Hi. I'm really glad to hear your program, and I just - my heart goes out to the author and any parents that deal with addiction. Because I actually lost my brother in 1995. He was 38. And I saw my parents from the time I was born practically trying to handle him. And he was brilliant. I mean, he had an IQ over 160. He was an incredible con artist, very charming, but he was born right in the midst of all the drugs in the 1960s, and, you know, he was just ripe for the taking.",
        "And, you know, he could quit for a while, but it was almost as if they were afraid to just let him go. Even though he did live on the street, they thought they'd find him dead in a ditch somewhere. Instead, they found him in their garage on April day, and with heroin and cocaine and some other barbiturates in his system.",
        "And, you know, it's just - I just wanted to throw out the fact that a lot of people think, oh, 30 days in treatment will take care of it. A lot of people don't get better. And a lot of people, as your guests know, can go in and out of treatment a million times. And it's a very tricky disease - and cunning, baffling and powerful, they say in the program. And, you know, I just - I'm glad to hear, you know, the information, but I just want to say that it's a tragic thing for parents to deal with. And I never thought that anything could destroy my parents, you know, as you do as a child. And they lived through it, but they were never the same.",
        "CONAN: Nobody's ever the same, Leslie.", "LESLIE: I'm sorry?", "CONAN: Nobody's ever the same.",
        "LESLIE: You're right. You're right. And I, you know, I just - trying to help often will hurt. And, you know, I don't have the answers, that's for sure, but I'm just glad to hear it out on the airwaves. Thanks so much.",
        'CONAN: And thanks so much for the call. I wanted to end with this email we have from Elizabeth in San Jose. I\'m the mother of a recovering addict. David\'s book was the catalyst for me in reaching out for help for myself. The night I checked my then-15-year-old son into an inpatient rehab facility, I sat and read "A Beautiful Boy" cover to cover, thinking it held the answer to fixing my son.',
        "While the book does not offer a cure for addiction, it gave me a sense I was not a lone in this struggle, and I subsequently reached out for help from others who suffer due to the addiction of a friend or loved one through a worldwide organization called Nar-Anon. And Elizabeth, thank you very much for the email. Thanks to everybody who called and wrote. I'm sorry we couldn't get to everybody's story. David  Sheff, thanks for your time.",
        'SHEFF: Thank you, Neal.',
        'CONAN: David Sheff joined us from KQED. And our thanks as well to Dr. Terry Schneekloth at the Mayo Clinic. This is TALK OF THE NATION from NPR News.']
    transcript_len = len(sentences)
    avg = math.floor(transcript_len / 2)

    index = 1
    for i, sent in enumerate(sentences):
        if utterance in sent:
            index = i
            break

    return 2 if index > avg else 1

#Trimming
def main(audio_dir, utterance, context):
    segment = localize_segment(utterance)
    trimmed_audio = pf.split_audio(audio_dir, segment)
    trim_file_name = pf.write_audio(trimmed_audio, audio_dir)

    pipe = pipeline(
        task="automatic-speech-recognition",
        model="openai/whisper-small",  # change to tiny/base/small/medium/large/large-v2 as required
        chunk_length_s=30,
        device=device,
    )

    out = pipe(trim_file_name, return_timestamps=True)["chunks"]
    print(out)

if __name__ == "__main__":
    audio = "C:\\Users\\kyvin\\PycharmProjects\\QuantNeg_Webcrawler\\audio_processing\\npr_addiction.mp3"; utterance = "So eventually, you know, that's where I got. I got to the point that, you know, I realized that everything I was doing was not helping him"; context = ""
    main(audio, utterance, context)