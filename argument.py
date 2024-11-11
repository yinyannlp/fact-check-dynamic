import argparse


def create_argparser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--datasets", type=str, default=None,
                        help="available datasets: [Feverous, Hover, ClaimDecompose, AVeriTeC, PubHealth, Liar_raw, RawFC,COVIDFACT]")
    parser.add_argument("--baseline", type=str, default=None,
                        help="available baselines: [ProgramFC, Wice, FactScore, ClaimDecompose, PropSegment, Coling]")
    parser.add_argument("--model",type=str,default=None,
                        help="available models: [ChatGPT, Llama2, Qwen]")
    args = parser.parse_args()

    return args