"""Export the embedded speaker notes as a printable rehearsal script."""
import os

from pptx import Presentation

DECK = "/home/user/viva/Chike_Egonu_Viva_Presentation.pptx"
OUT = "/home/user/viva/presentation/Viva_Speaker_Script.md"


# slide number -> the one sentence that has to land (seconds are derived from notes)
LAND = {
    1: "Who I am, what the project is, and that two results were not expected.",
    2: "One aim, three objectives, and Objective 3 is only a first pass.",
    3: "Implicit feedback is ambiguous, so explanation is about interpretation, not decoration.",
    4: "Intrinsic models are a constraint here; SHAP and LIME are the post-hoc route.",
    5: "Four gaps in the literature, each one tied to a design decision.",
    6: "150,000 playlists reduce to 96,827 users and 1.93 million interactions.",
    7: "The acoustic features are skewed and correlated, which matters for Section 4.3.",
    8: "Late fusion keeps the content contribution separable, which is what makes attribution possible.",
    9: "Five models, one protocol, so every difference is a model difference.",
    10: "The surrogate replaces DeepExplainer, and R-squared of 0.105 is the price.",
    11: "The hybrid beats NCF on all four metrics at K = 10.",
    12: "SVD-MF is ahead, but the neural models are at five epochs, so that ranking is provisional.",
    13: "Instrumentalness dominates globally, and the two methods order features differently on one item.",
    14: "Mean rho of 0.008 across 200 instances: no consistent agreement between SHAP and LIME.",
    15: "Four validity threats, and each one has a stated remedy.",
    16: "One outcome confirmed, one not observed, one pending, one new.",
    17: "Training to convergence is first, and the user study is last for a reason.",
    18: "Three results and what is still open.",
    19: "Hand over to questions.",
}
WPS = 2.45          # words per second, i.e. about 147 words a minute
BACKUP = {20: "References", 21: "Four questions I expect", 22: "Reported numbers"}


def biggest_title(slide):
    best, size = "", 0
    for sh in slide.shapes:
        if not sh.has_text_frame:
            continue
        for p in sh.text_frame.paragraphs:
            for r in p.runs:
                s = r.font.size.pt if r.font.size else 0
                txt = r.text.strip()
                if txt.isdigit() or (txt and all(c in "0123456789 \u00b7." for c in txt)):
                    continue          # skip the giant section numeral
                if s > size and txt:
                    size, best = s, sh.text_frame.text.strip().split("\n")[0]
    return best


def main():
    prs = Presentation(DECK)
    lines = ["# Viva speaker script",
             "",
             "**Explainable Music Recommender Systems for Improving User Satisfaction**  ",
             "Chike Egonu · Supervisor: Aoife Curran · August 2026",
             "",
             "22 slides: 19 presented and 3 backup. The script runs about 13 minutes at a "
             "measured pace, which leaves roughly 2 minutes of slack in a 15-minute slot.",
             "",
             "## Beat sheet",
             "",
             "| Slide | Seconds | Cumulative | The sentence that has to land |",
             "| --- | --- | --- | --- |",
             ]
    acc = 0
    for n in sorted(LAND):
        slide = prs.slides[n - 1]
        words = 0
        if slide.has_notes_slide:
            words = len(slide.notes_slide.notes_text_frame.text.split())
        secs = max(8, round(words / WPS))
        acc += secs
        lines.append(f"| {n:02d} | {secs} | {acc // 60}:{acc % 60:02d} | {LAND[n]} |")
    lines += ["",
              f"Spoken total {acc // 60}:{acc % 60:02d}. The 15-minute slot leaves roughly "
              f"{(900 - acc) // 60}:{(900 - acc) % 60:02d} for the walk to the lectern, "
              "transitions and the handover to questions.",
              "",
              "Slides 20-22 are backup only. They stay in the file so a question can be "
              "answered with a slide, but they are never presented: "
              + "; ".join(f"{n} {t}" for n, t in BACKUP.items()) + ".",
              "",
              "---",
              ""]
    for i, slide in enumerate(prs.slides, start=1):
        title = biggest_title(slide)
        note = ""
        if slide.has_notes_slide:
            note = slide.notes_slide.notes_text_frame.text.strip()
        tag = "  ·  BACKUP, not presented" if i in BACKUP else ""
        lines.append(f"## Slide {i:02d} — {title or '(no title)'}{tag}")
        lines.append("")
        if note:
            for para in note.split("\n"):
                lines.append(para.rstrip())
        else:
            lines.append("_No notes on this slide — section divider or reference material. "
                         "Signpost verbally and move on._")
        lines.append("")
        lines.append("---")
        lines.append("")
    with open(OUT, "w") as f:
        f.write("\n".join(lines))
    print(f"wrote {OUT} ({len(lines)} lines)")


if __name__ == "__main__":
    main()
