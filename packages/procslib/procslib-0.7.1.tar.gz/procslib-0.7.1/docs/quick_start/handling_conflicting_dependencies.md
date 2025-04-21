# Handling Conflicting dependencies

(todo: more on that later)

Q-align和siglip aesthetics 2.5不兼容; 两者只能单独使用.

- Q-align: 需要`pip install "transformers==4.36.1"`

- siglip aesthetics: 需要更高版本的transformers `pip install -U transformers`

inference之后重新安装transformers来切换可用的模型版本