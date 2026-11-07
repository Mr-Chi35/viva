"""Assemble the viva deck."""
import sys

import deck_lib as d
import sec_a_front as a
import sec_b_method as b
import sec_c_results as c
import sec_d_back as e

OUT = "/home/user/viva/Chike_Egonu_Viva_Presentation.pptx"


def main():
    prs = d.new_deck()
    page = 2  # title slide is page 1
    page = a.build(prs, page)
    page = b.build(prs, page)
    page = c.build(prs, page)
    page = e.build(prs, page)

    cp = prs.core_properties
    cp.title = ("Explainable Music Recommender Systems for Improving User Satisfaction "
                "\u2014 Viva presentation")
    cp.author = "Chike Egonu"
    cp.subject = "MSc dissertation \u2014 scientific report defence"
    cp.keywords = ("explainable recommendation; music recommender systems; SHAP; LIME; "
                   "neural collaborative filtering; Spotify MPD")
    cp.comments = ("42 slides: 35 content + 7 appendix. Speaker notes on every content slide.")
    cp.category = "Presentation"

    d.save(prs, OUT)

    n = len(prs.slides.__iter__.__self__._sldIdLst)
    print(f"slides: {n}   last page number: {page - 1}")
    warns = d.warnings()
    if warns:
        print(f"\n{len(warns)} layout warnings:")
        for w in warns:
            print("  -", w)
    else:
        print("\nno layout warnings")


if __name__ == "__main__":
    sys.exit(main())
