# AAIRE Complete System Documentation & Module Index

**Scanned Directory:** `/home/runner/work/AAIRE/AAIRE/aaire_core`
**Total Modules Documented:** 54

---

## Module: `skill_manager`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/skill_manager.py`
- **Description:** No module docstring provided.
- **Total Functions:** 4

### Functions:
  - `def __init__()`: No description.
  - `def register_skill()`: किसी नए स्किल या प्लगइन को सिस्टम में रजिस्टर करता है।
  - `def execute_skill()`: रजिस्टर किए गए स्किल को उसके नाम से कॉल करता है।
  - `def list_skills()`: उपलब्ध सभी स्किल्स की सूची देता है।

---

## Module: `mcts_reasoner`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/mcts_reasoner.py`
- **Description:** UCB1 Monte-Carlo Tree Search & Bayesian Decision Engine.
- **Total Functions:** 4

### Functions:
  - `def ucb1_score()`: No description.
  - `def __init__()`: No description.
  - `def update_bayesian_belief()`: No description.
  - `def search_optimal_strategy()`: No description.

---

## Module: `code_analyzer`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/code_analyzer.py`
- **Description:** No module docstring provided.
- **Total Functions:** 3

### Functions:
  - `def __init__()`: No description.
  - `def analyze_source_code()`: सोर्स कोड को पार्स करके उसके फंक्शन्स, इम्पोर्ट्स और संभावित कमियों की रिपोर्ट देता है।
  - `def analyze_code_metrics()`: कोड के मेट्रिक्स और स्टेटस की त्वरित जांच के लिए सहायक मेथड।

---

## Module: `visual_monitor`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/visual_monitor.py`
- **Description:** No module docstring provided.
- **Total Functions:** 3

### Functions:
  - `def __init__()`: No description.
  - `def update_status()`: एजेंट की स्थिति को अपडेट करता है और प्रोग्रेस प्रिंट करता है।
  - `def render_progress_card()`: टास्क की प्रगति का विजुअल कार्ड तैयार करता है।

---

## Module: `model_router`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/model_router.py`
- **Description:** No module docstring provided.
- **Total Functions:** 2

### Functions:
  - `def __init__()`: No description.
  - `def route_request()`: टास्क के प्रकार के आधार पर मॉडल और पैरामीटर्स तय करता है।

---

## Module: `semantic_memory`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/semantic_memory.py`
- **Description:** Local TF-IDF Vector Search & SQLite Episodic Memory Engine.
- **Total Functions:** 6

### Functions:
  - `def __init__()`: No description.
  - `def _init_db()`: No description.
  - `def _tokenize()`: No description.
  - `def store_memory()`: No description.
  - `def _cosine_similarity()`: No description.
  - `def recall()`: No description.

---

## Module: `auto_docs`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/auto_docs.py`
- **Description:** No module docstring provided.
- **Total Functions:** 5

### Functions:
  - `def __init__()`: No description.
  - `def scan_and_document_all_modules()`: पूरे फोल्डर को स्कैन करता है और सभी पाइथन मॉड्यूल्स के फंक्शन्स और डॉकस्ट्रिंग्स निकालता है।
  - `def _extract_doc_from_file()`: सहायक मेथड: किसी एक फाइल से उसकी जानकारी और फंक्शन्स निकालता है।
  - `def generate_markdown_summary()`: स्कैन किए गए सभी मॉड्यूल्स की जानकारी से एक सुंदर मार्डाउन (Markdown) रिपोर्ट तैयार करता है।
  - `def generate_changelog_entry()`: नया चेंजलॉग प्रविष्टि मार्डाउन फॉर्मेट में तैयार करता है।

---

## Module: `dag_engine`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/dag_engine.py`
- **Description:** Part 9: DAG Task Dependency Resolver & Sub-Agent Execution Engine.
- **Total Functions:** 5

### Functions:
  - `def __init__()`: No description.
  - `def build_dag_tasks()`: No description.
  - `def resolve_dag_waves()`: No description.
  - `def _synthesize_agent_code()`: No description.
  - `def execute_task()`: No description.

---

## Module: `genetic_optimizer`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/genetic_optimizer.py`
- **Description:** Genetic AST Code Profiler (CPU Nanoseconds + Memory Allocation) & Skill Evolver.
- **Total Functions:** 4

### Functions:
  - `def __init__()`: No description.
  - `def _is_ast_safe()`: No description.
  - `def evolve_best_variant()`: No description.
  - `def _save_winner()`: No description.

---

## Module: `dynamic_tool_forge`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/dynamic_tool_forge.py`
- **Description:** No module docstring provided.
- **Total Functions:** 2

### Functions:
  - `def __init__()`: No description.
  - `def forge_tool()`: एक नया पायथन टूल फाइल के रूप में लिखता है और उसे उपयोग के लिए तैयार करता है।

---

## Module: `thought_graph`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/thought_graph.py`
- **Description:** No module docstring provided.
- **Total Functions:** 5

### Functions:
  - `def __init__()`: No description.
  - `def _load_graph()`: लोकल स्टोरेज से पुराना थॉट ग्राफ लोड करता है।
  - `def _save_graph()`: थॉट ग्राफ को सुरक्षित रूप से फाइल में सेव करता है।
  - `def add_thought_node()`: नए थॉट नोड या एपिसोडिक अनुभव को ग्राफ में जोड़ता है।
  - `def get_past_insights()`: समान गोल्स या पुरानी रणनीतियों के आधार पर सीखे गए अनुभवों को ढूंढता है।

---

## Module: `config`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/config.py`
- **Description:** Part 1: AAIRE v4.1 Configuration, Constants & Zero-Trust Forbidden Rules.
- **Total Functions:** 1

### Functions:
  - `def utc_now()`: No description.

---

## Module: `error_classifier`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/error_classifier.py`
- **Description:** No module docstring provided.
- **Total Functions:** 2

### Functions:
  - `def __init__()`: No description.
  - `def classify_and_prescribe()`: एरर को एनालाइज करके उसका प्रकार और रिकवरी एक्शन बताता है।

---

## Module: `approval_gate`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/approval_gate.py`
- **Description:** No module docstring provided.
- **Total Functions:** 2

### Functions:
  - `def __init__()`: No description.
  - `def request_approval()`: किसी संवेदनशील टास्क के लिए अप्रूवल मांगता है या ऑटो-अप्रूव मोड की जाँच करता है।

---

## Module: `oracle_pipeline`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/oracle_pipeline.py`
- **Description:** AAIRE Commercial B2B Zero-Rot Verified Data Oracle Pipeline.
- **Total Functions:** 2

### Functions:
  - `def __init__()`: No description.
  - `def generate_verified_feed()`: No description.

---

## Module: `merkle_storage`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/merkle_storage.py`
- **Description:** Part 8: Atomic Storage, Cryptographic Merkle State Ledger & DLQ Autopsy.
- **Total Functions:** 7

### Functions:
  - `def __init__()`: No description.
  - `def atomic_write_json()`: No description.
  - `def append_merkle_state()`: No description.
  - `def verify_merkle_ledger()`: No description.
  - `def rollback_to_last_valid_state()`: No description.
  - `def update_learned_patterns()`: No description.
  - `def dump_to_dlq_autopsy()`: No description.

---

## Module: `swarm_executor`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/swarm_executor.py`
- **Description:** No module docstring provided.
- **Total Functions:** 2

### Functions:
  - `def __init__()`: No description.
  - `def run()`: No description.

---

## Module: `consensus_engine`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/consensus_engine.py`
- **Description:** No module docstring provided.
- **Total Functions:** 3

### Functions:
  - `def __init__()`: No description.
  - `def submit_proposal()`: विभिन्न एजेंट्स से प्रपोजल या समाधान स्वीकार करता है।
  - `def reach_consensus()`: सभी प्रपोजल्स का विश्लेषण करता है और सबसे अधिक स्कोर वाले सर्वमान्य समाधान को चुनता है।

---

## Module: `semantic_rag_vault`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/semantic_rag_vault.py`
- **Description:** No module docstring provided.
- **Total Functions:** 5

### Functions:
  - `def __init__()`: No description.
  - `def _load_memory()`: लोकल स्टोरेज से पुरानी मेमोरी लोड करता है।
  - `def _save_memory()`: मेमोरी को सुरक्षित रूप से फाइल में सेव करता है।
  - `def add_knowledge()`: नया ज्ञान या कोड स्निपेट मेमोरी में जोड़ता है।
  - `def search_knowledge()`: क्वेरी के आधार पर स्थानीय मेमोरी से प्रासंगिक जानकारी ढूंढता है।

---

## Module: `ast_guard`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/ast_guard.py`
- **Description:** Part 5: Zero-Trust AST Sandbox, Complexity Profiler & Self-Correction.
- **Total Functions:** 3

### Functions:
  - `def _extract_call_name()`: No description.
  - `def inspect_code()`: No description.
  - `def reflective_self_correct()`: Strips dangerous patterns or repairs broken syntax blocks automatically.

---

## Module: `resilience`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/resilience.py`
- **Description:** Part 4: Dynamic Circuit Breaker & Adaptive Concurrency Governor.
- **Total Functions:** 5

### Functions:
  - `def __init__()`: No description.
  - `def allow()`: No description.
  - `def record_success()`: No description.
  - `def record_failure()`: No description.
  - `def compute_workers()`: No description.

---

## Module: `master_orchestrator`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/master_orchestrator.py`
- **Description:** No module docstring provided.
- **Total Functions:** 3

### Functions:
  - `def __init__()`: No description.
  - `def run_unified_kernel()`: No description.
  - `def kernel_execution_logic()`: No description.

---

## Module: `credential_vault`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/credential_vault.py`
- **Description:** No module docstring provided.
- **Total Functions:** 6

### Functions:
  - `def __init__()`: No description.
  - `def _load_vault()`: सुरक्षित स्टोरेज से क्रेडेंशियल्स लोड करता है।
  - `def _save_vault()`: क्रेडेंशियल्स को एन्क्रिप्टेड या सुरक्षित तरीके से फाइल में सेव करता है।
  - `def set_credential()`: किसी गुप्त की (API Key / Token) को वॉल्ट में स्टोर करता है।
  - `def get_credential()`: वॉल्ट या पर्यावरण चर (Environment Variables) से क्रेडेंशियल प्राप्त करता है।
  - `def list_keys()`: स्टोर किए गए क्रेडेंशियल कीज़ की सूची देता है (वैल्यू छुपाकर)।

---

## Module: `prompt_cache_manager`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/prompt_cache_manager.py`
- **Description:** No module docstring provided.
- **Total Functions:** 4

### Functions:
  - `def __init__()`: No description.
  - `def set_cached_prompt()`: प्रॉम्प्ट या सिस्टम इंस्ट्रक्शन को कैच में सेव करता है।
  - `def get_cached_prompt()`: यदि कैच मौजूद है और एक्सपायर नहीं हुआ है, तो उसे रिटर्न करता है।
  - `def clear_cache()`: कैच को पूरी तरह साफ करता है।

---

## Module: `quantum_mesh_kernel`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/quantum_mesh_kernel.py`
- **Description:** Asyncio Actor Mesh Bus with 3-State Self-Healing Circuit Breaker.
- **Total Functions:** 6

### Functions:
  - `def __init__()`: No description.
  - `def can_execute()`: No description.
  - `def record_success()`: No description.
  - `def record_failure()`: No description.
  - `def __init__()`: No description.
  - `def subscribe()`: No description.

---

## Module: `telegram_gateway`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/telegram_gateway.py`
- **Description:** No module docstring provided.
- **Total Functions:** 3

### Functions:
  - `def __init__()`: No description.
  - `def register_command_handler()`: किसी विशेष टेलीग्राम कमांड (जैसे /status, /deploy) के लिए फंक्शन रजिस्टर करता है।
  - `def handle_incoming_webhook()`: टेलीग्राम या अन्य वेबहुक से मिलने वाले पेलोड को पार्स और हैंडल करता है।

---

## Module: `local_agent`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/local_agent.py`
- **Description:** Part 10: AAIRE v4.1 Master Brain Orchestrator & CLI Entrypoint.
- **Total Functions:** 7

### Functions:
  - `def main()`: No description.
  - `def __init__()`: No description.
  - `def _setup_logger()`: No description.
  - `def _register_events()`: No description.
  - `def log()`: No description.
  - `def run_self_diagnostics()`: No description.
  - `def run()`: No description.

---

## Module: `knowledge_spider`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/knowledge_spider.py`
- **Description:** No module docstring provided.
- **Total Functions:** 3

### Functions:
  - `def __init__()`: No description.
  - `def parse_dynamic_content()`: दिए गए HTML कंटेंट को डायनामिकली पार्स करता है और शीर्षक, लिंक्स, 
कीवर्ड्स तथा प्रासंगिक डेटा को अलग करता है।
  - `def get_spider_stats()`: स्पाइडर द्वारा अब तक क्रॉल किए गए डेटा का आँकड़ा देता है।

---

## Module: `swarm_priority_queue`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/swarm_priority_queue.py`
- **Description:** No module docstring provided.
- **Total Functions:** 4

### Functions:
  - `def __init__()`: No description.
  - `def enqueue_task()`: टास्क को उसकी प्राथमिकता (छोटा नंबर = उच्च प्राथमिकता) के साथ क्यू में जोड़ता है।
  - `def process_next_task()`: अगले उच्च-प्राथमिकता वाले टास्क को निकालकर निष्पादित (Execute) करता है।
  - `def get_queue_stats()`: क्यू की वर्तमान स्थिति और इतिहास का आँकड़ा देता है।

---

## Module: `memory_tot`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/memory_tot.py`
- **Description:** Part 7: Semantic Episodic Memory & Tree-of-Thoughts (ToT) Planner.
- **Total Functions:** 6

### Functions:
  - `def __init__()`: No description.
  - `def _tokenize()`: No description.
  - `def _cosine_sim()`: No description.
  - `def recall_best()`: No description.
  - `def store_episode()`: No description.
  - `def select_optimal_strategy()`: No description.

---

## Module: `models`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/models.py`
- **Description:** Part 2: AAIRE v4.1 Task State Machine & Data Models.
- **Total Functions:** 0

---

## Module: `self_critic`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/self_critic.py`
- **Description:** No module docstring provided.
- **Total Functions:** 2

### Functions:
  - `def __init__()`: No description.
  - `def evaluate_output()`: एआई के आउटपुट का क्रिटिकल विश्लेषण करता है।

---

## Module: `context_compressor`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/context_compressor.py`
- **Description:** No module docstring provided.
- **Total Functions:** 3

### Functions:
  - `def __init__()`: No description.
  - `def compress_text()`: टेक्स्ट को संक्षिप्त करता है और अनावश्यक खाली जगहों को साफ करता है।
  - `def optimize_chat_history()`: चैट इतिहास में से केवल हाल के महत्वपूर्ण संदेशों को रखता है ताकि मेमोरी ओवरलोड न हो।

---

## Module: `browser_agent`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/browser_agent.py`
- **Description:** No module docstring provided.
- **Total Functions:** 2

### Functions:
  - `def __init__()`: No description.
  - `def navigate_and_extract()`: दिए गए यूआरएल पर नेविगेट करके डेटा या स्ट्रक्चर एक्सट्रैक्ट करता है।

---

## Module: `verify_runner`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/verify_runner.py`
- **Description:** No module docstring provided.
- **Total Functions:** 3

### Functions:
  - `def __init__()`: No description.
  - `def verify_code_integrity()`: कोड की सिंटैक्स शुद्धता और संभावित रनटाइम कमियों की जांच करता है।
  - `def run_safe_pytest()`: सुरक्षित रूप से यूनिट टेस्ट्स (pytest) निष्पादित करता है।

---

## Module: `webhook_manager`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/webhook_manager.py`
- **Description:** No module docstring provided.
- **Total Functions:** 3

### Functions:
  - `def __init__()`: No description.
  - `def register_webhook()`: किसी विशेष इवेंट के लिए वेबहुक रूट रजिस्टर करता है।
  - `def handle_incoming_payload()`: आने वाले वेबहुक पेलोड को प्रोसेस करके संबंधित कॉलबैक निष्पादित करता है।

---

## Module: `latency_tracer`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/latency_tracer.py`
- **Description:** No module docstring provided.
- **Total Functions:** 3

### Functions:
  - `def __init__()`: No description.
  - `def measure_execution()`: किसी भी फंक्शन या टास्क को रन करके उसकी लेटेसी (मिलीसेकंड में) मापता है।
  - `def get_performance_summary()`: सभी रिकॉर्ड किए गए ट्रेसेस का परफॉरमेंस समरी देता है।

---

## Module: `consensus`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/consensus.py`
- **Description:** Part 6: Multi-Agent Weighted Consensus Voting Protocol.
- **Total Functions:** 1

### Functions:
  - `def evaluate()`: No description.

---

## Module: `mesh_bus`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/mesh_bus.py`
- **Description:** Part 3: Distributed Event-Driven Pub/Sub Bus & Thread-Safe Blackboard.
- **Total Functions:** 7

### Functions:
  - `def __init__()`: No description.
  - `def subscribe()`: No description.
  - `def publish()`: No description.
  - `def __init__()`: No description.
  - `def write()`: No description.
  - `def read()`: No description.
  - `def snapshot()`: No description.

---

## Module: `secure_sandbox`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/secure_sandbox.py`
- **Description:** No module docstring provided.
- **Total Functions:** 3

### Functions:
  - `def __init__()`: No description.
  - `def validate_command_safety()`: जांचता है कि कमांड में कोई खतरनाक या प्रतिबंधित कोड तो नहीं है।
  - `def run_sandboxed_snippet()`: छोटे पायथन स्निपेट को सुरक्षित रूप से सबप्रोसेस में रन करके रिजल्ट देता है।

---

## Module: `completed_thirteen`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/tools_partial_13/completed_thirteen.py`
- **Description:** No module docstring provided.
- **Total Functions:** 5

### Functions:
  - `def __init__()`: No description.
  - `def handle_starttag()`: No description.
  - `def decompile_pyinstaller_bytecode()`: No description.
  - `def verify_apk_and_evm_full()`: No description.
  - `def analyze_website_linear_145x()`: No description.

---

## Module: `magic_sniffer`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/detector_25/magic_sniffer.py`
- **Description:** No module docstring provided.
- **Total Functions:** 1

### Functions:
  - `def sniff_artifact()`: No description.

---

## Module: `native_inspectors`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/tools_binaries/native_inspectors.py`
- **Description:** No module docstring provided.
- **Total Functions:** 2

### Functions:
  - `def scan_entropy()`: No description.
  - `def inspect_binary_surface()`: No description.

---

## Module: `app_data_tools`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/tools_web_js_data/app_data_tools.py`
- **Description:** No module docstring provided.
- **Total Functions:** 2

### Functions:
  - `def inspect_js_and_models()`: No description.
  - `def inspect_sqlite_readonly()`: No description.

---

## Module: `apk_dotnet_tools`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/tools_mobile_managed/apk_dotnet_tools.py`
- **Description:** No module docstring provided.
- **Total Functions:** 1

### Functions:
  - `def analyze_mobile_or_dotnet()`: No description.

---

## Module: `true_generator`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/agi_synthesizer/true_generator.py`
- **Description:** No module docstring provided.
- **Total Functions:** 2

### Functions:
  - `def __init__()`: No description.
  - `def generate_fullstack_app()`: No description.

---

## Module: `quality_gate`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/quality_gate/quality_gate.py`
- **Description:** No module docstring provided.
- **Total Functions:** 4

### Functions:
  - `def to_dict()`: No description.
  - `def __init__()`: No description.
  - `def validate_python_code()`: No description.
  - `def validate_agent_output()`: No description.

---

## Module: `completed_four`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/tools_missing_4/completed_four.py`
- **Description:** No module docstring provided.
- **Total Functions:** 4

### Functions:
  - `def decompile_native_pseudocode()`: No description.
  - `def inspect_linux_coredump()`: No description.
  - `def inspect_jeb_project()`: No description.
  - `def decode_sigrok_capture()`: No description.

---

## Module: `cross_os_vault`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/security_crypto/cross_os_vault.py`
- **Description:** No module docstring provided.
- **Total Functions:** 4

### Functions:
  - `def __init__()`: No description.
  - `def create_public_seal()`: No description.
  - `def is_safe_url()`: No description.
  - `def scan_windowed_chunks()`: No description.

---

## Module: `mcp_skills_hub`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/skills_11_mcp/mcp_skills_hub.py`
- **Description:** No module docstring provided.
- **Total Functions:** 2

### Functions:
  - `def parse_local_intent()`: No description.
  - `def handle_mcp_rpc()`: No description.

---

## Module: `decomposer`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/task_decomposer/decomposer.py`
- **Description:** No module docstring provided.
- **Total Functions:** 4

### Functions:
  - `def to_dict()`: No description.
  - `def spawn_agent_for_task()`: No description.
  - `def __init__()`: No description.
  - `def decompose()`: No description.

---

## Module: `hardware_supervisor`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/edge_cluster/hardware_supervisor.py`
- **Description:** No module docstring provided.
- **Total Functions:** 2

### Functions:
  - `def __init__()`: No description.
  - `def probe_hardware_and_supervise()`: No description.

---

## Module: `visual_telemetry`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/edge_cluster/visual_telemetry.py`
- **Description:** No module docstring provided.
- **Total Functions:** 2

### Functions:
  - `def __init__()`: No description.
  - `def render_visual_dashboard()`: No description.

---

## Module: `container_forge`
- **Path:** `/home/runner/work/AAIRE/AAIRE/aaire_core/edge_cluster/container_forge.py`
- **Description:** No module docstring provided.
- **Total Functions:** 2

### Functions:
  - `def __init__()`: No description.
  - `def synthesize_cluster_spec()`: No description.

---

