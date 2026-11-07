"""Export the embedded speaker notes as a printable rehearsal script."""
import os

from pptx import Presentation

DECK = "/home/user/viva/Chike_Egonu_Viva_Presentation.pptx"
OUT = "/home/user/viva/presentation/Viva_Speaker_Script.md"


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
             "42 slides: 35 presentation + 7 appendix. Target running time ≈ 19 minutes of "
             "content. Timing hints are included at the top of each note block.",
             "",
             "---",
             ""]
    for i, slide in enumerate(prs.slides, start=1):
        title = biggest_title(slide)
        note = ""
        if slide.has_notes_slide:
            note = slide.notes_slide.notes_text_frame.text.strip()
        lines.append(f"## Slide {i:02d} — {title or '(no title)'}")
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
