import os
import sys
import json
import tempfile

import pandas as pd
import gradio as gr

from gradio_i18n import Translate, gettext as _

from test_api import test_api_connection
from cache_utils import setup_workspace, cleanup_workspace
from count_tokens import count_tokens

# pylint: disable=wrong-import-position
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from graphgen.graphgen import GraphGen
from graphgen.models import OpenAIModel, Tokenizer, TraverseStrategy
from graphgen.models.llm.limitter import RPM, TPM

css = """
.center-row {
    display: flex;
    justify-content: center;
    align-items: center;
}
"""

def init_graph_gen(config: dict, env: dict) -> GraphGen:
    # Set up working directory
    working_dir = setup_workspace(os.path.join(root_dir, "cache"))

    graph_gen = GraphGen(
        working_dir=working_dir
    )

    # Set up LLM clients
    graph_gen.synthesizer_llm_client = OpenAIModel(
        model_name=env.get("SYNTHESIZER_MODEL", ""),
        base_url=env.get("SYNTHESIZER_BASE_URL", ""),
        api_key=env.get("SYNTHESIZER_API_KEY", ""),
        request_limit=True,
        rpm= RPM(env.get("RPM", 1000)),
        tpm= TPM(env.get("TPM", 50000)),
    )

    graph_gen.trainee_llm_client = OpenAIModel(
        model_name=env.get("TRAINEE_MODEL", ""),
        base_url=env.get("TRAINEE_BASE_URL", ""),
        api_key=env.get("TRAINEE_API_KEY", ""),
        request_limit=True,
        rpm= RPM(env.get("RPM", 1000)),
        tpm= TPM(env.get("TPM", 50000)),
    )

    graph_gen.tokenizer_instance = Tokenizer(
        config.get("tokenizer", "cl100k_base"))

    strategy_config = config.get("traverse_strategy", {})
    graph_gen.traverse_strategy = TraverseStrategy(
        qa_form=config.get("qa_form"),
        expand_method=strategy_config.get("expand_method"),
        bidirectional=strategy_config.get("bidirectional"),
        max_extra_edges=strategy_config.get("max_extra_edges"),
        max_tokens=strategy_config.get("max_tokens"),
        max_depth=strategy_config.get("max_depth"),
        edge_sampling=strategy_config.get("edge_sampling"),
        isolated_node_strategy=strategy_config.get("isolated_node_strategy"),
        loss_strategy=str(strategy_config.get("loss_strategy")),
        # difficulty_order=strategy_config.get("difficulty_order", ["medium", "medium", "medium"])
    )

    return graph_gen

# pylint: disable=too-many-statements
def run_graphgen(*arguments: list, progress=gr.Progress()):
    def sum_tokens(client):
        return sum(u["total_tokens"] for u in client.token_usage)

    # Unpack arguments
    config = {
        "if_trainee_model": arguments[0],
        "input_file": arguments[1],
        "tokenizer": arguments[2],
        "qa_form": arguments[3],
        "web_search": False,
        "quiz_samples": 2,
        "traverse_strategy": {
            "bidirectional": arguments[4],
            "expand_method": arguments[5],
            "max_extra_edges": arguments[6],
            "max_tokens": arguments[7],
            "max_depth": arguments[8],
            "edge_sampling": arguments[9],
            "isolated_node_strategy": arguments[10],
            "loss_strategy": arguments[11],
            # "difficulty_order": [arguments[10]] * 3
        },
        "chunk_size": arguments[16],
    }

    env = {
        "SYNTHESIZER_BASE_URL": arguments[12],
        "SYNTHESIZER_MODEL": arguments[13],
        "TRAINEE_BASE_URL": arguments[12],
        "TRAINEE_MODEL": arguments[14],
        "SYNTHESIZER_API_KEY": arguments[15],
        "TRAINEE_API_KEY": arguments[15],
        "RPM": arguments[17],
        "TPM": arguments[18],
    }

    # Test API connection
    test_api_connection(env["SYNTHESIZER_BASE_URL"],
                        env["SYNTHESIZER_API_KEY"], env["SYNTHESIZER_MODEL"])

    # Initialize GraphGen
    graph_gen = init_graph_gen(config, env)
    graph_gen.clear()

    graph_gen.progress_bar = progress

    try:
        # Load input data
        file = config['input_file']
        if isinstance(file, list):
            file = file[0]

        data = []

        if file.endswith(".jsonl"):
            data_type = "raw"
            with open(file, "r", encoding='utf-8') as f:
                data.extend(json.loads(line) for line in f)
        elif file.endswith(".json"):
            data_type = "chunked"
            with open(file, "r", encoding='utf-8') as f:
                data.extend(json.load(f))
        elif file.endswith(".txt"):
            # 读取文件后根据chunk_size转成raw格式的数据
            data_type = "raw"
            content = ""
            with open(file, "r", encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    content += line.strip() + " "
            size = int(config.get("chunk_size", 512))
            chunks = [
                content[i:i + size] for i in range(0, len(content), size)
            ]
            data.extend([{"content": chunk} for chunk in chunks])
        else:
            raise ValueError(f"Unsupported file type: {file}")

        # Process the data
        graph_gen.insert(data, data_type)

        if config['if_trainee_model']:
            # Generate quiz
            graph_gen.quiz(max_samples=quiz_samples)

            # Judge statements
            graph_gen.judge()
        else:
            graph_gen.traverse_strategy.edge_sampling = "random"
            # Skip judge statements
            graph_gen.judge(skip=True)

        # Traverse graph
        graph_gen.traverse()

        # Save output
        output_data = graph_gen.qa_storage.data
        with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".jsonl",
                delete=False,
                encoding="utf-8") as tmpfile:
            json.dump(output_data, tmpfile, ensure_ascii=False)
            output_file = tmpfile.name

        synthesizer_tokens = sum_tokens(graph_gen.synthesizer_llm_client)
        trainee_tokens = sum_tokens(graph_gen.trainee_llm_client) if config['if_trainee_model'] else 0
        total_tokens = synthesizer_tokens + trainee_tokens

        data_frame = arguments[-1]
        try:
            data_frame = arguments[-1]
            _update_data = [
                [
                    data_frame.iloc[0, 0],
                    data_frame.iloc[0, 1],
                    str(total_tokens)
                ]
            ]
            new_df = pd.DataFrame(
                _update_data,
                columns=data_frame.columns
            )
            data_frame = new_df

        except Exception as e:
            raise gr.Error(f"DataFrame operation error: {str(e)}")

        return output_file, gr.DataFrame(label='Token Stats',
                         headers=["Source Text Token Count", "Expected Token Usage", "Token Used"],
                         datatype=["str", "str", "str"],
                         interactive=False,
                         value=data_frame,
                         visible=True,
                         wrap=True)

    except Exception as e:  # pylint: disable=broad-except
        raise gr.Error(f"Error occurred: {str(e)}")

    finally:
        # Clean up workspace
        cleanup_workspace(graph_gen.working_dir)


with (gr.Blocks(title="GraphGen Demo", theme=gr.themes.Glass(),
               css=css) as demo):
    # Header
    gr.Image(value=os.path.join(root_dir, 'resources', 'images', 'logo.png'),
             label="GraphGen Banner",
             elem_id="banner",
             interactive=False,
             container=False,
             show_download_button=False,
             show_fullscreen_button=False)
    lang_btn = gr.Radio(
        choices=[
            ("English", "en"),
            ("简体中文", "zh"),
        ],
        value="en",
        # label=_("Language"),
        render=False,
        container=False,
        elem_classes=["center-row"],
    )

    gr.HTML("""
    <div style="display: flex; gap: 8px; margin-left: auto; align-items: center; justify-content: center;">
        <a href="https://github.com/open-sciencelab/GraphGen/releases">
            <img src="https://img.shields.io/badge/Version-v0.1.0-blue" alt="Version">
        </a>
        <a href="https://graphgen-docs.example.com">
            <img src="https://img.shields.io/badge/Docs-Latest-brightgreen" alt="Documentation">
        </a>
        <a href="https://github.com/open-sciencelab/GraphGen">
            <img src="https://img.shields.io/github/stars/open-sciencelab/GraphGen?style=social" alt="GitHub Stars">
        </a>
        <a href="https://arxiv.org/xxxxx">
            <img src="https://img.shields.io/badge/arXiv-xxxxx-yellow" alt="arXiv">
        </a>
    </div>
    """)
    with Translate(
            os.path.join(root_dir, 'webui', 'translation.json'),
            lang_btn,
            placeholder_langs=["en", "zh"],
            persistant=
            False,  # True to save the language setting in the browser. Requires gradio >= 5.6.0
    ):
        lang_btn.render()

        gr.Markdown(
            value = "# " + _("Title") + "\n\n" + \
                "### [GraphGen](https://github.com/open-sciencelab/GraphGen) " + _("Intro")
        )

        if_trainee_model = gr.Checkbox(label=_("Use Trainee Model"),
                                       value=False,
                                       interactive=True)

        with gr.Accordion(label=_("Model Config"), open=False):
            base_url = gr.Textbox(label="Base URL",
                                  value="https://api.siliconflow.cn/v1",
                                  info=_("Base URL Info"),
                                  interactive=True)
            synthesizer_model = gr.Textbox(label="Synthesizer Model",
                                           value="Qwen/Qwen2.5-7B-Instruct",
                                           info=_("Synthesizer Model Info"),
                                           interactive=True)
            trainee_model = gr.Textbox(
                label="Trainee Model",
                value="Qwen/Qwen2.5-7B-Instruct",
                info=_("Trainee Model Info"),
                interactive=True,
                visible=if_trainee_model.value is True)

        with gr.Accordion(label=_("Generation Config"), open=False):
            chunk_size = gr.Slider(label="Chunk Size",
                                   minimum=256,
                                   maximum=4096,
                                   value=512,
                                   step=256,
                                   interactive=True)
            tokenizer = gr.Textbox(label="Tokenizer",
                                   value="cl100k_base",
                                   interactive=True)
            qa_form = gr.Radio(choices=["atomic", "multi_hop", "open"],
                               label="QA Form",
                               value="open",
                               interactive=True)
            quiz_samples = gr.Number(label="Quiz Samples",
                                     value=2,
                                     minimum=1,
                                     interactive=True,
                                     visible=if_trainee_model.value is True)
            bidirectional = gr.Checkbox(label="Bidirectional",
                                        value=True,
                                        interactive=True)

            expand_method = gr.Radio(choices=["max_width", "max_tokens"],
                                     label="Expand Method",
                                     value="max_tokens",
                                     interactive=True)
            max_extra_edges = gr.Slider(
                minimum=1,
                maximum=10,
                value=5,
                label="Max Extra Edges",
                step=1,
                interactive=True,
                visible=expand_method.value == "max_width")
            max_tokens = gr.Slider(minimum=64,
                                   maximum=1024,
                                   value=256,
                                   label="Max Tokens",
                                   step=64,
                                   interactive=True,
                                   visible=(expand_method.value
                                            != "max_width"))

            max_depth = gr.Slider(minimum=1,
                                  maximum=5,
                                  value=2,
                                  label="Max Depth",
                                  step=1,
                                  interactive=True)
            edge_sampling = gr.Radio(
                choices=["max_loss", "min_loss", "random"],
                label="Edge Sampling",
                value="max_loss",
                interactive=True,
                visible=if_trainee_model.value is True)
            isolated_node_strategy = gr.Radio(choices=["add", "ignore"],
                                              label="Isolated Node Strategy",
                                              value="ignore",
                                              interactive=True)
            loss_strategy = gr.Radio(choices=["only_edge", "both"],
                                     label="Loss Strategy",
                                     value="only_edge",
                                     interactive=True)
            # difficulty_level = gr.Radio(choices=["easy", "medium", "hard"], label="Difficulty Level", value="medium")

        with gr.Row(equal_height=True):
            with gr.Column(scale=3):
                api_key = gr.Textbox(
                    label=_("SiliconCloud Token"),
                    type="password",
                    value="",
                    info="https://cloud.siliconflow.cn/account/ak")
            with gr.Column(scale=1):
                test_connection_btn = gr.Button(_("Test Connection"))

        with gr.Blocks():
            with gr.Row(equal_height=True):
                with gr.Column():
                    rpm = gr.Slider(
                        label="RPM",
                        minimum=10,
                        maximum=10000,
                        value=1000,
                        step=100,
                        interactive=True,
                        visible=True)
                with gr.Column():
                    tpm = gr.Slider(
                        label="TPM",
                        minimum=5000,
                        maximum=5000000,
                        value=50000,
                        step=1000,
                        interactive=True,
                        visible=True)


        with gr.Blocks():
            with gr.Row(equal_height=True):
                with gr.Column(scale=1):
                    upload_file = gr.File(
                        label=_("Upload File"),
                        file_count="single",
                        file_types=[".txt", ".json", ".jsonl"],
                        interactive=True,
                    )
                    examples_dir = os.path.join(root_dir, 'webui', 'examples')
                    gr.Examples(examples=[
                        [os.path.join(examples_dir, "txt_demo.txt")],
                        [os.path.join(examples_dir, "raw_demo.jsonl")],
                        [os.path.join(examples_dir, "chunked_demo.json")],
                    ],
                                inputs=upload_file,
                                label=_("Example Files"),
                                examples_per_page=3)
                with gr.Column(scale=1):
                    output = gr.File(
                        label="Output",
                        file_count="single",
                        interactive=False,
                    )

        with gr.Blocks():
            token_counter = gr.DataFrame(label='Token Stats',
                         headers=["Source Text Token Count", "Estimated Token Usage", "Token Used"],
                         datatype=["str", "str", "str"],
                         interactive=False,
                         visible=False,
                         wrap=True)

        submit_btn = gr.Button(_("Run GraphGen"))

        # Test Connection
        test_connection_btn.click(
            test_api_connection,
            inputs=[base_url, api_key, synthesizer_model],
            outputs=[])

        if if_trainee_model.value:
            test_connection_btn.click(test_api_connection,
                                    inputs=[base_url, api_key, trainee_model],
                                    outputs=[])

        expand_method.change(lambda method:
                             (gr.update(visible=method == "max_width"),
                              gr.update(visible=method != "max_width")),
                             inputs=expand_method,
                             outputs=[max_extra_edges, max_tokens])

        if_trainee_model.change(
            lambda use_trainee: (gr.update(visible=use_trainee is True),
                                 gr.update(visible=use_trainee is True),
                                 gr.update(visible=use_trainee is True)),
            inputs=if_trainee_model,
            outputs=[trainee_model, quiz_samples, edge_sampling])

        # 计算上传文件的token数
        upload_file.change(
            lambda x: (gr.update(visible=True)),
            inputs=[upload_file],
            outputs=[token_counter],
        ).then(
            count_tokens,
            inputs=[upload_file, tokenizer, token_counter],
            outputs=[token_counter],
        )

        # run GraphGen
        submit_btn.click(
            lambda x: (gr.update(visible=False)),
            inputs=[token_counter],
            outputs=[token_counter],
        ).then(
            run_graphgen,
            inputs=[
                if_trainee_model, upload_file, tokenizer, qa_form,
                bidirectional, expand_method, max_extra_edges, max_tokens,
                max_depth, edge_sampling, isolated_node_strategy,
                loss_strategy, base_url, synthesizer_model, trainee_model,
                api_key, chunk_size, rpm, tpm, token_counter
            ],
            outputs=[output, token_counter],
        )

if __name__ == "__main__":
    demo.queue(api_open=False, default_concurrency_limit=10)
    demo.launch(server_name='0.0.0.0')
