#! /usr/bin/env bash

function bluer_sandbox_offline_llm_prompt() {
    local options=$1
    local do_upload=$(bluer_ai_option_int "$options" upload 1)

    local prompt=$2
    bluer_ai_log "🗣️ $prompt"

    local object_name=$(bluer_ai_clarify_object $3 offline_llm-reply-$(bluer_ai_string_timestamp_short))
    local object_path=$ABCLI_OBJECT_ROOT/$object_name
    mkdir -pv $object_path

    echo "$prompt" >$object_path/prompt.txt

    pushd $abcli_path_git/llama.cpp >/dev/null
    ./build/bin/llama-cli \
        -m $ABCLI_OBJECT_ROOT/offline-llm-model-object/mistral-7b-instruct-v0.1.Q4_K_M.gguf \
        -p "$prompt" \
        -n 300 \
        --color \
        --temp 0.7 | tee $object_path/output.txt
    [[ $? -ne 0 ]] && return 1

    popd $abcli_path_git/llama.cpp >/dev/null

    python3 -m bluer_sandbox.offline_llm \
        post_process \
        --object_name $object_name
    [[ $? -ne 0 ]] && return 1

    [[ "$do_upload" == 1 ]] &&
        bluer_objects_upload - $object_name

    bluer_objects_mlflow_tags_set \
        $object_name \
        contains=offline_llm
}
