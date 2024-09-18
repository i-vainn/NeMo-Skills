import hashlib
import subprocess


def compute_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def test_multiple_files():
    output_file = "tests/data/processed_multifile_output.jsonl"
    subprocess.run(
        [
            "python",
            "nemo_skills/finetuning/prepare_sft_data.py",
            "input_files='tests/data/output-rs*.test'",
            f"output_path={output_file}",
            "prompt_config=llama3-instruct/math",
            "prompt_template=llama3-instruct",
            "exclude_optional_keys=false",
            "filters.drop_multi_boxed=true",
            "filters.drop_broken_code=true",
            "filters.trim_solutions=true",
            "filters.code_text_filter=null",
            "num_output_samples=null",
            "downsampling_method=null",
            "do_shuffle=false",
        ],
        check=True,
    )

    expected_md5 = "063633c0d2b4c69f3926127edf845fa7"
    output_md5 = compute_md5(output_file)

    assert (
        expected_md5 == output_md5
    ), "MD5 hashes do not match, something is wrong with nemo_skills/finetuning/prepare_sft_data.py"


def test_exclude_keys():
    output_file = "tests/data/processed_compact_output.jsonl"
    subprocess.run(
        [
            "python",
            "nemo_skills/finetuning/prepare_sft_data.py",
            "input_files='tests/data/output-rs*.test'",
            f"output_path={output_file}",
            "prompt_config=llama3-instruct/math",
            "prompt_template=llama3-instruct",
            "exclude_optional_keys=true",
            "filters.drop_multi_boxed=true",
            "filters.drop_broken_code=true",
            "filters.trim_solutions=true",
            "filters.code_text_filter=null",
            "num_output_samples=null",
            "downsampling_method=null",
            "do_shuffle=false",
        ],
        check=True,
    )

    expected_md5 = "d4726dddf111fc1712b4248f43425837"
    output_md5 = compute_md5(output_file)

    assert (
        expected_md5 == output_md5
    ), "MD5 hashes do not match, something is wrong with nemo_skills/finetuning/prepare_sft_data.py"


def test_openmathinstruct():
    output_file = "tests/data/processed_openmathinstruct_output.jsonl"

    subprocess.run(
        [
            "python",
            "nemo_skills/finetuning/prepare_sft_data.py",
            "preprocessed_dataset_files='tests/data/openmathinstruct.test'",
            f"output_path={output_file}",
            "prompt_config=llama3-instruct/math",
            "prompt_template=llama3-instruct",
            "exclude_optional_keys=false",
            "filters.drop_multi_boxed=true",
            "filters.drop_broken_code=true",
            "filters.trim_solutions=true",
            "filters.code_text_filter=any_code",
            "num_output_samples=32",
            "downsampling_method=fair",
            "do_shuffle=true",
        ],
        check=True,
    )

    expected_md5 = "3f22c685ec4deac09346656c14e6e946"
    output_md5 = compute_md5(output_file)

    assert (
        expected_md5 == output_md5
    ), "MD5 hashes do not match, something is wrong with nemo_skills/finetuning/prepare_sft_data.py"


def test_code_sft_data():
    output_file = "tests/data/code_processed_output.jsonl"
    subprocess.run(
        [
            "python",
            "nemo_skills/finetuning/prepare_sft_data.py",
            "--config-name=prepare_code_sft_data",
            "preprocessed_dataset_files='tests/data/code-output.test'",
            f"output_path={output_file}",
            "prompt_config=llama3-instruct/math",
            "prompt_template=llama3-instruct",
            "exclude_optional_keys=false",
            "filters.drop_incorrect_code_blocks=false",
            "generation_suffix='\"<|eot_id|>\"'",
        ],
        check=True,
    )

    expected_md5 = "c7d2859c6f17031f6b2256481b588336"
    output_md5 = compute_md5(output_file)

    assert (
        expected_md5 == output_md5
    ), "MD5 hashes do not match, something is wrong with nemo_skills/finetuning/prepare_sft_data.py"
