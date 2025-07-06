NOT COMPLETE:
Traceback (most recent call last):
  File "_pydevd_bundle\\pydevd_cython.pyx", line 2017, in _pydevd_bundle.pydevd_cython.ThreadTracer.__call__
  File "/Users/zhenzhili/.vscode/extensions/ms-python.debugpy-2025.6.0-darwin-arm64/bundled/libs/debugpy/_vendored/pydevd/_pydev_bundle/pydev_is_thread_alive.py", line 16, in is_thread_alive
    def is_thread_alive(t):
    
  File "/Users/zhenzhili/MASTERTHESIS/#Expert_System_Design/examples/LANGDA/#drone_with_dpl_in_langgraph_v6.4/utils/test_tools.py", line 17, in timeout_handler
    raise TimeoutError(f"Function timed out while processing file: {file_basename}")
TimeoutError: Function timed out while processing file: benchcalcu:rough.pl_run1

Sixth test
model: LangdaAgentDoubleDC
used nodes:
- generate_node: double_chain_agent
- evaluate_node: double_chain_agent
- summary_node: simple_agent
- multi round: 5