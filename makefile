generate:
	python ./nfs_complementares.py NFS/Originais NFS/Complementares NFS/Base

generate_and_send:
	python  ./nfs_complementares.py --envio-producao NFS/Originais NFS/Complementares NFS/Base 2921 42596 

generate_and_homo:
	python  ./nfs_complementares.py --envio-homologacao NFS/Originais NFS/Complementares NFS/Base 2921 42596 

limpeza:
	rm -rf ./NFS/Complementares/*
	rm -rf ./NFS/Dicts_original/*
	rm -rf ./consultas/*
	mv ./log/0_geral*.log .
	rm -rf ./log/*
