"""
Post 8 Spark profile threads to #proj-redesign-spark via SparkBot.
Saves thread timestamps to spark_threads.json for use in weekly reminders.
Run once — do NOT re-run or it will create duplicate threads.
"""
import json
import os
from dotenv import load_dotenv
from slack_bolt import App

load_dotenv()
app = App(token=os.environ["SLACK_BOT_TOKEN"])

# Mentor name → Slack user ID for @mentions
MENTOR_IDS = {
    "Kienan":    "U03HFG3GA5V",
    "Neil":      "U03U1BQCT27",
    "Neharika":  "U08LS8QAQGH",
    "Aron/Dan":  "U0811F0LL8L",
    "Aron":      "U0811F0LL8L",
    "Patrick":   "U03BGD55Z6Y",
    "Jorge":     "U08UAHXRRPF",
    "Moz":       "U0ALPPVN517",
    "Akash":     "U0823GYJ7K5",
    "Preston":   "U09UGAXG6GH",
    "Tom":       "U0604RVV4R5",
    "Sarah":     "U026G26GK38",
    "Dan":       "U09MWB7KQSX",
    "Prithvi":   "U09HN4MAWLD",
    "Leland":    "U05NSUAJFM1",
    "Matt":      "U0AFBA5810A",
}

def mentionify(names_str):
    """Convert 'Kienan, Neharika' → '<@U03HFG3GA5V>, <@U08LS8QAQGH>'"""
    parts = [n.strip() for n in names_str.split(",")]
    return ", ".join(
        f"<@{MENTOR_IDS[n]}>" if n in MENTOR_IDS else n
        for n in parts
    )

CHANNEL = os.environ["SUMMARY_CHANNEL_ID"]

SPARKS = [
    {
        "name": "Aryan Srivastava",
        "linkedin": "https://linkedin.com/in/aryan-srivastava-9b1664185",
        "ashby": "https://app.ashbyhq.com/candidate-searches/new/right-side/candidates/dcf0c8a3-a991-4f09-81c1-83a65d672205",
        "mentors": {
            "Concept Vision": "Kienan, Neharika",
            "Founder DNA": "Tom, Sarah",
            "Tech / AI": "Aron, Dan",
            "Commercial": "Leland, Matt",
        },
        "scorecards": [
            {
                "interviewer": "Preston Tollinger",
                "date": "Feb 20",
                "score": "4/4",
                "text": "Other than a lack of go-to-market, Aryan is super strong. Built multiple things before. Moves fast. Knows how to figure out product fit. Has already tried to start a couple of things before deciding the market was too small. Kind of naive about healthcare at a deeper level — Kienan can really help him shape an idea. Wants and needs a co-founder.",
                "next_steps": "Settle on area of focus with Kienan + match with CEO/GTM co-founder",
            },
            {
                "interviewer": "Kienan O'Brien",
                "date": "Mar 2",
                "score": "3/4",
                "text": "Good rationale for the spaces he was originally interested in. Really excited to bring agentic innovation to multiple areas within healthcare. Seems pretty promising.",
                "next_steps": "Sent opportunity zone PDF — getting back with top 2-3 areas",
            },
        ],
    },
    {
        "name": "Rahul Kumar",
        "linkedin": "https://linkedin.com/in/rahulkumarm1",
        "ashby": "https://app.ashbyhq.com/candidate-searches/new/right-side/candidates/0ae3a2b7-ad35-446e-ab10-333b7c5ed444",
        "mentors": {
            "Concept Vision": "Neil, Jorge",
            "Founder DNA": "Tom, Sarah",
            "Tech / AI": "Dan, Prithvi",
            "Commercial": "Leland, Matt",
        },
        "scorecards": [
            {
                "interviewer": "Sarah Cranston",
                "date": "Feb 26",
                "score": "★ Favourite Spark",
                "text": "AI native, founder DNA, casual style, lots of depth, extremely mission driven and articulate communicating a vision. Humble/growth mindset. Had a co-founder he'd like to build with again who is going to med school. 'Founding a company in college was the most exciting time of my life.' Likes building consumer products, wants to directly interface with people.",
                "next_steps": None,
            },
            {
                "interviewer": "Kienan O'Brien",
                "date": "Mar 5",
                "score": "3/4",
                "text": "Walked through concept areas — exploring which opportunities resonated with his interest and skill set. Focused on consumer healthcare, insurance AI, and open evidence-type problems. Seems like a thoughtful person, maybe caught up a little too much in buzzier AI use cases than what he personally believes. Very open to thinking more deeply about specific healthcare applications and has the intelligence and technical acumen to tackle something exciting, not just buzzy.",
                "next_steps": None,
            },
            {
                "interviewer": "Harshel Bahl",
                "date": "Mar 18",
                "score": "3/4",
                "text": "He wasn't afraid to push back, which was a good thing. Definitely interested in the consumer side of healthcare. Something like Function Health is a good example of what was discussed. Also interested in an open evidence type of business that represents a hard technical problem. Technically strong and sharp overall, but quite inexperienced at understanding opportunity areas within healthcare. Not interested in more serious/boring problems like revenue cycle management.",
                "next_steps": None,
            },
        ],
    },
    {
        "name": "Daniel Nurieli",
        "linkedin": "https://linkedin.com/in/daniel-n-06484617b",
        "ashby": "https://app.ashbyhq.com/candidate-searches/new/right-side/candidates/76d4e1ba-0f39-4db2-9413-3b70865f66b3",
        "mentors": {
            "Concept Vision": "Aron/Dan, Neharika",
            "Founder DNA": "Tom, Sarah",
            "Tech / AI": "Dan, Prithvi",
            "Commercial": "Leland, Matt",
        },
        "scorecards": [
            {
                "interviewer": "Sarah Cranston",
                "date": "Mar 6",
                "score": "3/4",
                "text": "Touchbase on prior interview. Doing interesting work as a forward deployed engineer at Distillai — spun out of former Palantir employees, building GenAI agents for enterprises. Has worked closely with large enterprise clients including T-Mobile and Elevance Health. Wants to transition from employment to entrepreneurship. Recognizes need for domain knowledge and sees Redesign's ecosystem as highly valuable.",
                "next_steps": None,
            },
        ],
    },
    {
        "name": "Samuel Margolis",
        "linkedin": "https://linkedin.com/in/sam-margolis",
        "ashby": "https://app.ashbyhq.com/candidate-searches/new/right-side/candidates/a500af93-1ee7-48f2-ae13-e02f4b0cf658",
        "mentors": {
            "Concept Vision": "Patrick, Jorge, Moz",
            "Founder DNA": "Tom, Sarah",
            "Tech / AI": "Dan, Prithvi",
            "Commercial": "Leland, Matt",
        },
        "scorecards": [
            {
                "interviewer": "Tom Skiba",
                "date": "Mar 6",
                "score": "4/4",
                "text": "10/10 — ready to give him a check now, bypassed Concept Review. Perfect for Agents for X. Pure curious builder. Medical training + CS. Early research on adversarial attacks in ML. Founded and sold a digital marketing company in college for a few hundred thousand dollars. Worked at Gates Ventures for 2-3 years. Decided to pursue clinical medicine after a family health event — received a full ride to medical school. Published 14-15 research papers including work achieving state-of-the-art results for the GI specialty board exam. Built and open-sourced a scribe tool used by doctors at Stanford and NYP, with 30-40 collaborators. Currently building an open source library for monitoring and evaluation of agents in healthcare. Strong interest in trust/evaluation frameworks for AI deployment in clinical settings.",
                "next_steps": None,
            },
        ],
    },
    {
        "name": "Adedoyin & Chris",
        "linkedin": "https://linkedin.com/in/adedoyin-o",
        "ashby": "https://app.ashbyhq.com/candidate-searches/new/right-side/candidates/b8d34dda-13b9-4bc9-8872-309196a0ffe2",
        "mentors": {
            "Concept Vision": "Patrick, Neharika",
            "Founder DNA": "Tom, Sarah",
            "Tech / AI": "Dan, Prithvi",
            "Commercial": "Leland, Matt",
        },
        "scorecards": [
            {
                "interviewer": "Sarah Cranston",
                "date": "Mar 6",
                "score": "4/4",
                "text": "Love them both. Really nice pairing. Met on YC co-founder matching. Adedoyin = CEO/GTM (MIT CS + Econ, EMT experience, 1upHealth on health data interoperability, philanthropy/healthcare impact investing). Chris = CTO (co-founded Synapto — EEG device to diagnose Alzheimer's, won $40k in competitions; Flatiron Health — predicting outcomes in oncology; Blueberry Pediatrics — reducing ER visits for Medicaid; Fortuna Health — quit to launch this). Both deeply healthcare native with clearly defined roles and mutual respect. Chris has longstanding entrepreneurial motivation — second employee at Fortuna. Adedoyin gained confidence running business functions through investing + early-stage roles. Currently conducting customer discovery and ready to move quickly. Sarah immediately placed them in the top 3 to move forward with.",
                "next_steps": None,
            },
        ],
    },
    {
        "name": "Anmol Narula",
        "linkedin": "https://linkedin.com/in/anmol-narula",
        "ashby": "https://app.ashbyhq.com/candidate-searches/new/right-side/candidates/980004b5-6a23-439d-bca0-96ee7b48936f",
        "mentors": {
            "Concept Vision": "Neil, Akash",
            "Founder DNA": "Tom, Sarah",
            "Tech / AI": "Dan, Prithvi",
            "Commercial": "Leland, Matt",
        },
        "scorecards": [
            {
                "interviewer": "Preston Tollinger",
                "date": "Feb 20",
                "score": "4/4",
                "text": "Really liked Anmol for a young founder — other than not being an engineer he checks all the boxes. Doctors in the family, really understands many of the challenges. Good initial concept but excited to learn and find his wedges. In his final semester, goal is to found something. Previously started a CPG dairy startup in India. VC experience. Health tech research focus at Columbia. Looking for a technical co-founder — actively searching. If he came into the program with a technical co-founder, there's a reasonable chance he could make it through IC.",
                "next_steps": None,
            },
            {
                "interviewer": "Kienan O'Brien",
                "date": "Feb 23",
                "score": "2/4",
                "text": "Mainly focused on the opportunity in referrals and/or addressing no-shows. Underwhelmed — despite 3 months of exploring referral workflows, could only name 2 competitors and had only talked to a couple of clinicians. Spent most of the time with investors in Columbia's ecosystem. Thinking still immature. Concept may overlap with Corvus. Kienan later noted: 'I like the agent helping the patient — there's a downstream vision for Corvus to do some of that, but probably in future versions.' Re-added to Spark pool after further discussion.",
                "next_steps": None,
            },
            {
                "interviewer": "Preston Tollinger (Slack)",
                "date": "Feb 25",
                "score": None,
                "text": "Slightly more senior than other Sparks (5.5 YOE, more time in a startup), but thinking about how to explore the domain is still immature and could benefit from Spark. Focus area has overlap with Corvus — if we move ahead, he would need to be open to picking a different area. Also loses points for lack of deeper research in his chosen domain. Other option: have him get back to us if he finds a different area to explore.",
                "next_steps": None,
            },
            {
                "interviewer": "Neil Patel",
                "date": "Feb 27",
                "score": None,
                "text": "Deep concept session — Referral Completion Engine: AI agent that activates the moment a referral is triggered and drives it to completion (labs, insurance, prior auth, scheduling, patient nudges). Not a marketplace — active, not passive. Not clinical triage. Best initial GTM: health systems in fee-for-service tracking referral leakage (more completed referrals = more specialist visits in-network). VBC/ACOs are longer-term due to 12-18 month payback windows. Adjacent use cases: preventive screenings, care gap closures, HEDIS measures. Key distinction from Corvus: 'Corvus is air traffic controller for clinical decisions; Anmol's job is to close the loop once a referral is made.'",
                "next_steps": None,
            },
        ],
    },
    {
        "name": "Onkar Singh Gujral",
        "linkedin": "https://linkedin.com/in/onkar-singh-gujral-b9ab8626a",
        "ashby": "https://app.ashbyhq.com/candidate-searches/new/right-side/candidates/fa3e6435-4d40-45e9-98cd-1b8be53a8246",
        "mentors": {
            "Concept Vision": "Preston, Neharika",
            "Founder DNA": "Tom, Sarah",
            "Tech / AI": "Dan, Prithvi",
            "Commercial": "Leland, Matt",
        },
        "scorecards": [
            {
                "interviewer": "Preston Tollinger",
                "date": "Mar 3",
                "score": "4/4",
                "text": "Super smart guy excited to apply his PhD research in a startup. Previously started something in India in high school. PhD candidate in Applied Math at MIT — started in pure math, pivoted to applied AI. Research focus: AI interpretability for biology, specifically protein language models. Has a recent PNAS paper on PLM interpretability covered by MIT News and IBM Think. Wants to build the 'interpretability layer' between AI automation and high-stakes use cases, with healthcare as the initial vertical. Not training frontier models — focused on interpretability tooling and fine-tuning on existing models, which is compute-light and capital-efficient. Technically pragmatic, open to different wedges (model builders, model buyers, or intermediary). Sees Spark as structured exploration to refine the wedge and test customer types. Feels like a really interesting infrastructure-type play.",
                "next_steps": None,
            },
            {
                "interviewer": "Patrick McDonagh (Slack)",
                "date": "Mar 11",
                "score": None,
                "text": "In agreement with Preston — really like Onkar. Right in the bullseye: quite smart AI powerhouse who needs help on healthcare. Taught me a ton about Sparse Autoencoders in a surprisingly easy-to-follow way. Hard to understand if defensible as a company given it's a well-known approach — more about execution and distribution than IP. But Goodfire.AI raised $150M Series B at $1.25B valuation — good enough signal.",
                "next_steps": None,
            },
        ],
    },
    {
        "name": "Isabelle Gan",
        "linkedin": "https://linkedin.com/in/isabellegan",
        "ashby": "https://app.ashbyhq.com/candidate-searches/new/right-side/candidates/9259efa4-5313-40d8-a2cf-2e4f962f764a",
        "mentors": {
            "Concept Vision": "Kienan, Akash",
            "Founder DNA": "Tom, Sarah",
            "Tech / AI": "Dan, Prithvi",
            "Commercial": "Leland, Matt",
        },
        "scorecards": [
            {
                "interviewer": "Sarah Cranston",
                "date": "Mar 10",
                "score": "3/4",
                "text": "Extremely determined, smart, driven, desperate to be a founder — dropped out of Waterloo to pursue founding in SF. High potential, will need a lot of partnership. Started building in tech in high school: design, coding, MVP launches, pitch competitions. Investment analyst at Ripple Ventures. All work experience is temp/internships rather than full-time. Currently not working. Was working on a personal health companion app (aggregating labs, wearables) — pivoted away. Can design, code, and ship MVPs independently. 'If I can make even one life a little bit better because they have better access to their data, that would be so meaningful.' Sarah's take: inclined to take a risk on her.",
                "next_steps": None,
            },
            {
                "interviewer": "Patrick McDonagh",
                "date": "Mar 12",
                "score": "3/4",
                "text": "Isabelle is a tough one. Energy is pretty infectious, builder at heart, good intuition on how to build companies in the new age. No real track record given her age & recent Waterloo dropout. Main uncertainty: how we help her land on an idea. She's the 'willing to explore everything but unsure when she'll actually land on something' type — material risk she learns a lot but it doesn't form into anything. Closest concept fit: aggregating personal health data, Coro-like. Also a founder scout for Pear VC (PearX AI Female Founders Circle).",
                "next_steps": None,
            },
        ],
    },
]


def build_spark_blocks(spark):
    mentor_lines = "\n".join(
        f"• *{section}:* {mentionify(names)}" for section, names in spark["mentors"].items()
    )

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    f":sparkles: *{spark['name']}*\n"
                    f"<{spark['linkedin']}|LinkedIn>  ·  <{spark['ashby']}|Ashby Profile>\n\n"
                    f"*This thread is the running log for {spark['name']}. "
                    f"Drop your weekly updates, feedback, and observations here.*"
                ),
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f":busts_in_silhouette: *Mentors*\n{mentor_lines}"},
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": ":clipboard: *Pre-Spark Scorecards*"},
        },
    ]

    for sc in spark["scorecards"]:
        score_str = f" | {sc['score']}" if sc["score"] else ""
        header = f"*{sc['interviewer']}* _({sc['date']})_{score_str}"
        body = f">{sc['text']}"
        text = header + "\n" + body
        blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": text}})

    return blocks


def post_all_threads():
    results = {}

    for spark in SPARKS:
        blocks = build_spark_blocks(spark)
        resp = app.client.chat_postMessage(
            channel=CHANNEL,
            blocks=blocks,
            text=f"Spark: {spark['name']}",
        )
        ts = resp["ts"]
        results[spark["name"]] = {"ts": ts, "channel": CHANNEL}
        print(f"✅ Posted thread for {spark['name']} (ts: {ts})")

    with open("spark_threads.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ All 8 threads posted. Timestamps saved to spark_threads.json")


if __name__ == "__main__":
    post_all_threads()
