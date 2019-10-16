python3 ../../../../{{executable}} -d {{domain_decomposition_dirichlet}} -wr {{ wr_dirichlet }} {{ wr_neumann }} -dT {{ window_size }} -cpl {{ coupling_scheme }} -g {{gamma}} -tol {{error_tolerance}} -mth {{method}} -t {{time_dependence}} -wri {{waveform_interpolation_strategy}} --sdc-K {{sdc_K}} &
python3 ../../../../{{executable}} -n {{domain_decomposition_neumann}} -wr {{ wr_dirichlet }} {{ wr_neumann }} -dT {{ window_size }} -cpl {{ coupling_scheme }} -g {{gamma}} -tol {{error_tolerance}} -mth {{method}} -t {{time_dependence}} -wri {{waveform_interpolation_strategy}} --sdc-K {{sdc_K}}
