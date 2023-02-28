def assert_rounded_correct_num_decimals(on_offset_arr, decimals):
    __tracebackhide__ = True
    assert all([len(str(float(boundary_s)).split(".")[-1]) <= decimals for boundary_s in on_offset_arr])
