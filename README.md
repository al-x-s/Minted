# What is Minted?

Minted is a collaborative platform for hip hop producers and MC's to meet, collaborate and create original music. At it's heart it's about fostering a community of excellence amongst contributors and encourages this through community feedback, rankings and rewards.

## How does it work?

When users sign up to use the website they are given the option of creating a producer or MC account. Producers are able to upload beats and MC's can upload raps over those beats. All contributions can be rated by the community through "likes" and feedback can be given through comments. Top ranked contributions will appear on the home page increasing publicity for the contributors.

Visitors to the website can browse "beats" or "raps". When a user views a beat it will show all MC contributions on that beat.

# Why hip hop?

All music can be created through collaboration but some genres are better suited to online collaboration. The responsibilities of a producer and MC in the creation of hip hop are clearly delineated - a producer creates the beat (or the music) and the MC raps on top of the beat. This creative process makes hip hop an ideal candidate for online collaboration.

Hip hop also has a long tradition of MC's using other artists beats to express their ideas particularly in the pre and early stages of the internet. These raps were often labelled as "freestyles" and would appear on bootlegs or mixtapes and were generally used as promotional material. This practice began to die out as music piracy become more prominent and the music industry became more litigious.

Today some of the best produced beats in the world are made by "bedroom producers" (people at home making their own music and selling it online to production houses or directly to their favourite MC's). Whilst producers can sell their beats this way it's not often in their interest as poor performances on their music can impede them from getting public recognition. Similarly MC's can spend a lot of money on beats that aren't well suited to their style and it's a costly way of developing your sound as an artist. Minted hopes to provide new avenues for artist collaboration which avoids the risk of copyright infringement and allows artists to develop their sound whilst networking and promoting themselves.

# The Design

## UX

Ultimately minted is a social media platform built to foster an environment of creative collaboration. When wire-framing the website I knew I wanted user posts to appear in a similar format to a news feed or the front page of reddit with top rated content appearing front and centre.

## Challenges with The Audio Widget

Of all the components of the website that required the most attention to detail the music playback mechanism was a top-priority. Unfortunately it was also something that proved the most challenging.

Initially I had planned to use the Soundcloud API to host audio and then use the Soundcloud widget to render audio on the page but at this point in time Soundcloud were no longer allowing new developers to access their API. I attempted to use the Soundcloud widget regardless but without access to display the artist or track names properly the implementation was sloppy at best.

### Hosting Audio on Cloudinary

I eventually decided to allow users of the website to upload audio their own audio and to host the audio on Cloudinary. Ultimately this was a good decision as using Cloudinary also enabled me to allow users to upload profile pictures and album artwork which became an integral part of the webpages design.

I ended up using the Cloudinary upload widget to facilitate this which was probably overkill for what I needed but for a working demo of the website it did the job.

### Using the HTML Audio Element

This still left me with the challenge of finding a way to display the audio as a temporary measure I decided to use the HTML Audio Element which did the job but is not pretty! I did look at some pre-packaged Audio playback solutions for websites but did not have time to implement any. If I came back to the project this would be the first thing I looked at addressing. 

## CSS and Styling

There is much work to be done on this page with the styling but to my mind until I can find a satisfactory solution to the website audio playback I'm reluctant to develop the layout and style of the page. Many of the pre-packaged Audio playback solutions that I found online had vastly different styles and depending on which package I used (or even if I kept the HTML Audio element and redesigned it) I'd have to design the webpage around that solution.

# Database

## Learning SQL Alchemy and Postgres

In addition to the websites audio playback I found using SQL Alchemy to a real challenge that taught me a lot. Trying to wrap my head around my data models and how to set relationships between tables took me a couple of attempts to get right but in the end I got it right.

The website has 3 tables. One for it's Users, one for all Beats uploaded to the website, and another for the Raps uploaded to the website. Here are the models:

```
class  Users(db.Model):
	id  =  db.Column(db.Integer, primary_key=True)
	profile_pic  =  db.Column(db.String(500), nullable=False)
	account_type  =  db.Column(db.String(20), nullable=False)
	username  =  db.Column(db.String(50), unique=True, nullable=False)
	email  =  db.Column(db.String(80), unique=True, nullable=False)
	pw_hash  =  db.Column(db.String(100), nullable=False)

	user_beats  =  db.relationship("Beats", backref="user")
	user_tracks  =  db.relationship("Raps", backref="user")

class  Beats(db.Model):
	id  =  db.Column(db.Integer, primary_key=True)
	track_name  =  db.Column(db.String(100), nullable=False)
	uploaded_time  =  db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	artwork_url  =  db.Column(db.String(500), nullable=False)
	audio_url  =  db.Column(db.String(500), nullable=False)
	likes  =  db.Column(db.Integer, default=0)

	fk_user_id  =  db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

	rap_beat  =  db.relationship("Raps", backref="beat")

class  Raps(db.Model):
	id  =  db.Column(db.Integer, primary_key=True)
	uploaded_time  =  db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	audio_url  =  db.Column(db.String(500), nullable=False)
	likes  =  db.Column(db.Integer, default=0)

	user_id  =  db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
	beat_id  =  db.Column(db.Integer, db.ForeignKey("beats.id"), nullable=False)
```

Having a link between the Beats and their Users allowed me to display producer profile pictures when pulling data from the Beats table, and having the Raps linked to the Beats enabled me to display the relationship between collaborators. Whilst all this may be common sense to an experienced developer it enabled me to truly understand how a well designed databse can supercharge a website.

In addition to the generous assistance I always receive from General Assembly's tutors I would also like to acknowledge that I had an enormous amount of help from a YouTuber named Anthony Herbert who has a [page called "Pretty Printed".](https://www.youtube.com/@prettyprinted). Anthony really had a way to explaining database concepts that solidified my understanding. He even had video's on uploading your Flask projects to Render.com which I benefitted greatly from!

## Database Challenges

One of the difficulties I found with working with databases is that there were several points in time where I realised I'd need to add or modify something in my database in order to add functionality to the website. Due to the links between different tables it wasn't always as simple as modifying the tables that I had and on two occasions I had to re-initiate my databases from scratch. This was a very tedious process and I'm sure there are better workflows but it's something I'd need to experiment with.

# Future Features

## Minting NFT's

One major feature that is mentioned on the home page but is not currently in the websites design is the ability for users to mint an NFT of their collaborations. This was unfortunately outside of what I was going to be able to achieve in a week but there would be many benefits of allowing users to do this:

1. If a producer and MC agree to that they would like to turn their collaboration in an NFT it would be a record of ownership by both parties.
2. This would also establish the work as an original piece and if the artists wished to copyright the work it would prevent others who may have downloaded the producers beat from using the music (legally) after the NFT was created. This would also include the producer or MC themselves who could choose to recycle their music or lyrics.
3. With a record of ownership both parties could then register the piece with a collection society to claim royalties on any use of the music.

There's a lot of exciting things happening in web 3 with digital ownership. Websites like Royal.io are allowing established artists to connect with their fans by offering them a percentage of their royalties which is then held as an NFT by the fan. I believe this sort of public distribution could be harnessed to great effect between collaborators online.