import re

def guess_event_type(description: str) -> int:
    """
    Since Blaseball's live updates don't contain the convenient event type flag
    that the game feed event objects have, this method attempts to infer the 
    event type of an update based on its description.
    """
    # Lord forgive the things I do
    if re.match('let\'s go!', description, re.IGNORECASE | re.MULTILINE):
        return 0
    if re.match('play ball!', description, re.IGNORECASE | re.MULTILINE):
        return 1
    if re.match(r'(?:top|bottom) of \d+', description, re.IGNORECASE | re.MULTILINE):
        return 2
    if re.match('is now pitching', description, re.IGNORECASE | re.MULTILINE):
        return 3
    if re.match(r'(?:steals|gets caught stealing) \w+ base', description, re.IGNORECASE | re.MULTILINE):
        return 4
    if re.match(r'(?:draws a walk|walks to \w+ base|The umpire sends them to \w+ base|is intentionally walked)', description, re.IGNORECASE | re.MULTILINE):
        return 5
    if re.match(r'strikes? out (?:looking|swinging|thinking|willingly)', description, re.IGNORECASE | re.MULTILINE):
        return 6
    if re.match('hit a flyout', description, re.IGNORECASE | re.MULTILINE):
        return 7
    if re.match(r'(?:hit a ground out|out at \w+ base|hit into a \w+ play)', description, re.IGNORECASE | re.MULTILINE):
        return 8
    if re.match(r'hits a (?:(?:solo|\d+-run) home run|grand slam)', description, re.IGNORECASE | re.MULTILINE):
        return 9
    if re.match(r'hits a (?:single|double|triple|quadruple)', description, re.IGNORECASE | re.MULTILINE):
        return 10
    # if re.match('???', description, re.IGNORECASE | re.MULTILINE):
    #     return 11
    if re.match(r'(?:batting for|skipped up to bat)', description, re.IGNORECASE | re.MULTILINE):
        return 12
    if re.match(r'strike, (?:looking|swinging|flinching)', description, re.IGNORECASE | re.MULTILINE):
        return 13
    if re.match(r'^ball\.\s+\d+-\d+', description, re.IGNORECASE | re.MULTILINE):
        return 14
    if re.match(r'foul balls?.\s+\d+-\d+', description, re.IGNORECASE | re.MULTILINE):
        return 15
    if re.match('runs are overflowing', description, re.IGNORECASE | re.MULTILINE):
        return 20
    if re.match(r'hits .+ with a pitch', description, re.IGNORECASE | re.MULTILINE):
        return 22
    if re.match(r'is (?:elsewhere|shelled)', description, re.IGNORECASE | re.MULTILINE):
        return 23
    if re.match('is partying!', description, re.IGNORECASE | re.MULTILINE):
        return 24
    if re.match('zaps a strike away', description, re.IGNORECASE | re.MULTILINE):
        return 25
    if re.match('the polarity shifted', description, re.IGNORECASE | re.MULTILINE):
        return 26
    if re.match('throws a mild pitch', description, re.IGNORECASE | re.MULTILINE): # There's no way this won't match up with 5 or 14 first
        return 27
    if re.match(r'inning \d+ is now an outing', description, re.IGNORECASE | re.MULTILINE):
        return 28
    if re.match(r'swallow(s|ed) the runs', description, re.IGNORECASE | re.MULTILINE):
        return 30
    if re.match('sun 2 smile(s|ed)', description, re.IGNORECASE | re.MULTILINE):
        return 31
    if re.match(r'birds circle .+ don.t find what they.re looking for', description, re.IGNORECASE | re.MULTILINE):
        return 33
    if re.match('a murder of crows', description, re.IGNORECASE | re.MULTILINE):
        return 34
    if re.match(r'birds circle .+ pecked .+ free', description, re.IGNORECASE | re.MULTILINE):
        return 35
    if re.match(r'chugs? a third wave of coffee', description, re.IGNORECASE | re.MULTILINE):
        return 36
    if re.match(r'is poured over with a .+ roast', description, re.IGNORECASE | re.MULTILINE):
        return 37
    if re.match(r'is beaned by a .+ roast', description, re.IGNORECASE | re.MULTILINE):
        return 39
    if re.match(r'reality begins to flicker.+but .+ resists', description, re.IGNORECASE | re.MULTILINE | re.DOTALL):
        return 40
    if re.match(r'reality flickers.+switch teams in the flicker', description, re.IGNORECASE | re.MULTILINE | re.DOTALL):
        return 41
    if re.match('had a superallergic reaction', description, re.IGNORECASE | re.MULTILINE):
        return 45
    if re.match('had an allergic reaction', description, re.IGNORECASE | re.MULTILINE):
        return 47
    if re.match('is now reverberating wildly', description, re.IGNORECASE | re.MULTILINE):
        return 48
    if re.match(r'(were|had (several players|their lineup|their rotation)) shuffled in the reverb', description, re.IGNORECASE | re.MULTILINE):
        return 49
    if re.match(r'siphoned some of .+\s .+ ability', description, re.IGNORECASE | re.MULTILINE):
        return 51
    if re.match(r's siphon activates', description, re.IGNORECASE | re.MULTILINE):
        return 52
    if re.match('tried to siphon blood', description, re.IGNORECASE | re.MULTILINE):
        return 53
    if re.match('rogue umpire incinerated', description, re.IGNORECASE | re.MULTILINE):
        return 54
    if re.match('rogue umpire tried to incinerate', description, re.IGNORECASE | re.MULTILINE):
        return 55
    if re.match('baserunners are swept from play', description, re.IGNORECASE | re.MULTILINE):
        return 62
    if re.match('the salmon swim upstream', description, re.IGNORECASE | re.MULTILINE):
        return 63
    if re.match('enters the secret base', description, re.IGNORECASE | re.MULTILINE):
        return 65
    if re.match('exits the secret base', description, re.IGNORECASE | re.MULTILINE):
        return 66
    if re.match(r'(?:consumers attack|a consumer)', description, re.IGNORECASE | re.MULTILINE):
        return 67
    if re.match(r'is temporarily (reverberat|repeat)ing', description, re.IGNORECASE | re.MULTILINE):
        return 69
    if re.match('hops on the grind rail', description, re.IGNORECASE | re.MULTILINE):
        return 70
    if re.match(r'(?:entered the tunnels|attempted a heist)', description, re.IGNORECASE | re.MULTILINE):
        return 71
    if re.match(r'(?:is no longer superallergic|has been cured of their peanut allergy)', description, re.IGNORECASE | re.MULTILINE):
        return 72
    if re.match('tastes the infinite', description, re.IGNORECASE | re.MULTILINE):
        return 74
    if re.match('event horizon activates', description, re.IGNORECASE | re.MULTILINE):
        return 76
    if re.match('the solar panels absorb sun 2.s energy', description, re.IGNORECASE | re.MULTILINE):
        return 79
    if re.match(r'(has )?(returned|rolled back|was pulled back) from elsewhere', description, re.IGNORECASE | re.MULTILINE):
        return 84
    if re.match(r'over under, (off|on)', description, re.IGNORECASE | re.MULTILINE):
        return 85
    if re.match(r'under over, (off|on)', description, re.IGNORECASE | re.MULTILINE):
        return 86
    if re.match('go undersea', description, re.IGNORECASE | re.MULTILINE):
        return 88
    if re.match(r'is (happy to be home|homesick)', description, re.IGNORECASE | re.MULTILINE):
        return 91
    if re.match('perks up', description, re.IGNORECASE | re.MULTILINE):
        return 93
    if re.match(r'echo .+ static', description, re.IGNORECASE | re.MULTILINE):
        return 112
    if re.match(r'.+ echoed .+', description, re.IGNORECASE | re.MULTILINE):
        return 169
    if re.match('psychoacoustics echo', description, re.IGNORECASE | re.MULTILINE):
        return 173
    if re.match(r'echo .+ echo .+ echo', description, re.IGNORECASE | re.MULTILINE):
        return 174
    if re.match('a shimmering crate descends', description, re.IGNORECASE | re.MULTILINE):
        return 177
    if re.match(r'(is feeling|loses their) ambitio(us|n)', description, re.IGNORECASE | re.MULTILINE):
        return 182
    if re.match('is feeling unambitious', description, re.IGNORECASE | re.MULTILINE):
        return 183
    if re.match(r'consumers attack.+breaks?', description, re.IGNORECASE | re.MULTILINE | re.DOTALL):
        return 185
    if re.match(r'consumers attack.+damaged', description, re.IGNORECASE | re.MULTILINE | re.DOTALL):
        return 186
    if re.match('the community chest opens', description, re.IGNORECASE | re.MULTILINE):
        return 189
    if re.match('incoming shadow fax', description, re.IGNORECASE | re.MULTILINE):
        return 191
    if re.match('hotel motel', description, re.IGNORECASE | re.MULTILINE):
        return 192
    if re.match('prize match', description, re.IGNORECASE | re.MULTILINE):
        return 193
    if re.match(r'smithy beckons.+repaired', description, re.IGNORECASE | re.MULTILINE | re.DOTALL):
        return 195
    if re.match(r'.+ entered the vault', description, re.IGNORECASE | re.MULTILINE):
        return 196
    if re.match(r'the .+ have a blood type', description, re.IGNORECASE | re.MULTILINE):
        return 198
    if re.match('practice moderation', description, re.IGNORECASE | re.MULTILINE):
        return 208
    if re.match('game over.', description, re.IGNORECASE | re.MULTILINE):
        return 216
    if re.match(r'entered the tunnels.+but didn.t find anything interesting', description, re.IGNORECASE | re.MULTILINE | re.DOTALL):
        return 218
    if re.match(r'entered the tunnels.+but they were caught', description, re.IGNORECASE | re.MULTILINE | re.DOTALL):
        return 219
    if re.match(r'entered the tunnels.+caught their eye.+stole', description, re.IGNORECASE | re.MULTILINE | re.DOTALL):
        return 
    if re.match('sun 30 smiled upon them', description, re.IGNORECASE | re.MULTILINE):
        return 226
    if re.match('incoming voicemail', description, re.IGNORECASE | re.MULTILINE):
        return 228
    if re.match(r'stole .+ from .+ and gave it to .+', description, re.IGNORECASE | re.MULTILINE):
        return 230
    if re.match(r'stole .+ shadows player', description, re.IGNORECASE | re.MULTILINE):
        return 231
    if re.match(r'(?:sought out a trade|tried to trade with)', description, re.IGNORECASE | re.MULTILINE):
        return 234
    if re.match(r'(?:traitor|trader)? ?traded their .+', description, re.IGNORECASE | re.MULTILINE):
        return 236
    if re.match(r'pitcher .+ cycles out', description, re.IGNORECASE | re.MULTILINE):
        return 237
    if re.match('reloaded all of the bases', description, re.IGNORECASE | re.MULTILINE):
        return 239
    if re.match('a new weather report arrived', description, re.IGNORECASE | re.MULTILINE):
        return 243
    if re.match('game cancelled', description, re.IGNORECASE | re.MULTILINE):
        return 246
    if re.match('sun\(sun\) supernova', description, re.IGNORECASE | re.MULTILINE):
        return 247
    if re.match('black hole became agitated', description, re.IGNORECASE | re.MULTILINE):
        return 249
    if re.match(r'were (both )? nullified', description, re.IGNORECASE | re.MULTILINE):
        return 250
    if re.match('a riff opened', description, re.IGNORECASE | re.MULTILINE):
        return 251
    if re.match('deep darkness took', description, re.IGNORECASE | re.MULTILINE):
        return 252
    if re.match('became stuck', description, re.IGNORECASE | re.MULTILINE):
        return 254
    if re.match('horse power achieved', description, re.IGNORECASE | re.MULTILINE):
        return 255
    return None