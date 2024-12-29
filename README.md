# Twitch Drops Miner (Alpine)

Thanks to @DevilXD, @Windows200000, and other contributors from the [original repo](https://github.com/DevilXD/TwitchDropsMiner) and [forked repo](https://github.com/DevilXD/TwitchDropsMiner) for the vast majority of the code.

This modified version is designed run on Alpine Linux inside of a docker container. The [docker container repo](https://github.com/fireph/docker-twitch-drops-miner) has all the code to create a container with VNC and uploads it to Docker Hub. The notification tray functionality has been removed since that isn't needed for an app running inside Docker and causes the app size/container size to be much larger from the dependencies.

This application allows you to AFK mine timed Twitch drops, without having to worry about switching channels when the one you were watching goes offline, claiming the drops, or even receiving the stream data itself. This helps both you and Twitch save on bandwidth and hassle. Everyone wins!

### How It Works:

Every ~20 seconds, the application asks Twitch for a URL to the raw stream data of the channel currently being watched. It then fetches the metadata of this data stream - this is enough to advance the drops. Note that this completely bypasses the need to download any actual stream video and sound. To keep the status (ONLINE or OFFLINE) of the channels up-to-date, there's a websocket connection established that receives events about streams going up or down, or updates regarding the current amount of viewers.

### Features:

- Stream-less drop mining - save on bandwidth.
- Game priority and exclusion lists, allowing you to focus on mining what you want, in the order you want, and ignore what you don't want.
- Sharded websocket connection, allowing for tracking up to `8*25-2=199` channels at the same time.
- Automatic drop campaigns discovery based on linked accounts (requires you to do [account linking](https://www.twitch.tv/drops/campaigns) yourself though)
- Stream tags and drop campaign validation, to ensure you won't end up mining a stream that can't earn you the drop.
- Automatic channel stream switching, when the one you were currently watching goes offline, as well as when a channel streaming a higher priority game goes online.
- Login session is saved in a cookies file, so you don't need to login every time.
- Mining is automatically started as new campaigns appear, and stopped when the last available drops have been mined.

### Usage:

- Download and unzip [the latest release](https://github.com/fireph/TwitchDropsMiner-Alpine/releases) - it's recommended to keep it in the folder it comes in.
- Run it and login into your Twitch account using your username and password, and a 2FA key if you have one setup. It's recommended to avoid having to double-take this step, as you can run into CAPTCHA that will prevent you from trying to log in again for the next 12+ hours. You can retry afterwards though.
- After a successful login, the app should fetch a list of all available campaigns and games you can mine drops for - you can then select and add games of choice to the Priority List available on the Settings tab, and then press on the `Reload` button to start processing. It will fetch a list of all applicable streams it can watch, and start mining right away. You can also manually switch to a different channel as needed.
- Make sure to link your Twitch account to game accounts on the [campaigns page](https://www.twitch.tv/drops/campaigns), to enable more games to be mined.
- Persistent cookies will be stored in the `cookies.jar` file, from which the authorization (login) information will be restored on each subsequent run.

### Pictures:

![Main](https://user-images.githubusercontent.com/4180725/164298155-c0880ad7-6423-4419-8d73-f3c053730a1b.png)
![Inventory](https://user-images.githubusercontent.com/4180725/164298315-81cae0d2-24a4-4822-a056-154fd763c284.png)
![Settings](https://user-images.githubusercontent.com/4180725/164298391-b13ad40d-3881-436c-8d4c-34e2bbe33a78.png)
![Help](https://github.com/Windows200000/TwitchDropsMiner-updated/assets/72623832/ca1c25e1-650f-415b-ab9d-8cfc001fc7e6)


### Notes:

- Make sure to keep your cookies file safe, as the authorization information it stores can give another person access to your Twitch account.
- Successfully logging into your Twitch account in the application, may cause Twitch to send you a "New Login" notification email. This is normal - you can verify that it comes from your own IP address. The application uses the Twitch's SmartTV account linking process, so the detected browser during the login should signify that as well.
- The time remaining timer always countdowns a single minute and then stops - it is then restarted only after the application redetermines the remaining time. This "redetermination" can happen as early as at 10 seconds in a minute remaining, and as late as 20 seconds after the timer reaches zero (especially when finishing mining a drop), but is generally only an approximation and does not represent nor affect actual mining speed. The time variations are due to Twitch sometimes not reporting drop progress at all, or reporting progress for the wrong drop - these cases have all been accounted for in the application though.

### Notes about the Linux build:

- The Linux app is built and distributed using [PyInstaller](https://pyinstaller.org/).
- The Linux app should work out of the box on any modern distribution, as long as it uses `MUSL` (alternative to `glibc`), plus a working display server.
- Every feature of the app is expected to work on Linux just as well as it does on Windows. If you find something that's broken, please [open a new issue](https://github.com/DevilXD/TwitchDropsMiner/issues/new).

### Advanced Usage:

If you'd be interested in running the latest master from source or building your own executable, see the wiki page explaining how to do so: https://github.com/DevilXD/TwitchDropsMiner/wiki/Setting-up-the-environment,-building-and-running

### Credits:

<!---
Note: When adding a new credits line below, please add two spaces at the end of the previous line,
if they aren't already there. Doing so ensures proper markdown rendering on Github.

• Last line can have them omitted.
• Please ensure your editor won't trim the spaces upon saving the file.
• Please leave a single empty new line at the end of the file.
-->

@Suz1e - For the entirety of the Chinese (简体中文) translation and revisions.  
@wwj010 - For the Chinese (简体中文) translation corrections and revisions.  
@nwvh - For the entirety of the Czech (Čeština) translation.  
@ThisIsCyreX - For the entirety of the German (Deutsch) translation.  
@Shofuu - For the entirety of the Spanish (Español) translation.  
@zarigata - For the entirety of the Portuguese (Português) translation.  
@alikdb - For the entirety of the Turkish (Türkçe) translation.  
@roobini-gamer - For the entirety of the French (Français) translation.  
@Sergo1217 - For the entirety of the Russian (Русский) translation.  
@Ricky103403 - For the entirety of the Traditional Chinese (繁體中文) translation.  
@Patriot99 - For the Polish (Polski) translation (co-authored with @DevilXD).  
@Nollasko - For the entirety of the Ukrainian (Українська) translation.  
@casungo - For the entirety of the Italian (Italiano) translation.  
@Bamboozul - For the entirety of the Arabic (العربية) translation.  
@Kjerne - For the entirety of the Danish (Dansk) translation.

For updating Translations: @Kuddus73, @VSeryi, @Windows200000, @BreakshadowCN, @kilroy98, @zelda0079, @Calvineries, @notNSANE, @ElvisDesigns, @DogancanYr, @Nollasko, @rvpv, @flxderdev, @5wi5wi, @fgr1178707QQ, @Suz1e, @Patriot99, @overkongen, @zizimonzter, @sabala, @hiroweeb, @T-Raptor, @LoLyeah
